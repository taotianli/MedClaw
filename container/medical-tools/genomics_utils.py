#!/usr/bin/env python3
"""
Genomics Analysis Utilities for MedClaw
Provides helper functions for VCF, BAM, and sequence analysis
"""

import pysam
from Bio import SeqIO
from Bio.Seq import Seq
from pathlib import Path
from typing import List, Dict, Optional, Iterator
import json


def parse_vcf_file(vcf_path: str, quality_threshold: float = 20.0) -> List[Dict]:
    """
    Parse VCF file and extract variant information.

    Args:
        vcf_path: Path to VCF file
        quality_threshold: Minimum quality score for variants

    Returns:
        List of variant dictionaries
    """
    variants = []

    try:
        vcf_file = pysam.VariantFile(vcf_path)

        for record in vcf_file:
            if record.qual is None or record.qual >= quality_threshold:
                variant = {
                    'chromosome': record.chrom,
                    'position': record.pos,
                    'id': record.id if record.id else '.',
                    'reference': record.ref,
                    'alternate': [str(alt) for alt in record.alts] if record.alts else [],
                    'quality': float(record.qual) if record.qual else None,
                    'filter': list(record.filter) if record.filter else [],
                    'info': dict(record.info) if record.info else {}
                }
                variants.append(variant)

        vcf_file.close()
    except Exception as e:
        print(f"Error parsing VCF: {e}")

    return variants


def get_bam_statistics(bam_path: str) -> Dict:
    """
    Calculate statistics from BAM file.

    Args:
        bam_path: Path to BAM file

    Returns:
        Dictionary of statistics
    """
    stats = {
        'total_reads': 0,
        'mapped_reads': 0,
        'unmapped_reads': 0,
        'properly_paired': 0,
        'duplicates': 0,
        'chromosomes': {}
    }

    try:
        bamfile = pysam.AlignmentFile(bam_path, "rb")

        for read in bamfile:
            stats['total_reads'] += 1

            if read.is_unmapped:
                stats['unmapped_reads'] += 1
            else:
                stats['mapped_reads'] += 1

                # Count by chromosome
                chrom = read.reference_name
                if chrom not in stats['chromosomes']:
                    stats['chromosomes'][chrom] = 0
                stats['chromosomes'][chrom] += 1

            if read.is_proper_pair:
                stats['properly_paired'] += 1

            if read.is_duplicate:
                stats['duplicates'] += 1

        bamfile.close()

        # Calculate percentages
        if stats['total_reads'] > 0:
            stats['mapping_rate'] = stats['mapped_reads'] / stats['total_reads'] * 100
            stats['duplicate_rate'] = stats['duplicates'] / stats['total_reads'] * 100

    except Exception as e:
        print(f"Error reading BAM file: {e}")

    return stats


def get_coverage_at_position(bam_path: str, chromosome: str, position: int,
                             window: int = 0) -> Dict:
    """
    Get read coverage at a specific genomic position.

    Args:
        bam_path: Path to BAM file
        chromosome: Chromosome name
        position: Genomic position (1-based)
        window: Window size around position

    Returns:
        Dictionary with coverage information
    """
    try:
        bamfile = pysam.AlignmentFile(bam_path, "rb")

        start = max(0, position - window - 1)  # Convert to 0-based
        end = position + window

        coverage = []
        for pileup_column in bamfile.pileup(chromosome, start, end):
            coverage.append({
                'position': pileup_column.pos + 1,  # Convert to 1-based
                'depth': pileup_column.n
            })

        bamfile.close()

        return {
            'chromosome': chromosome,
            'position': position,
            'window': window,
            'coverage': coverage
        }

    except Exception as e:
        print(f"Error getting coverage: {e}")
        return {}


def parse_fasta_file(fasta_path: str) -> List[Dict]:
    """
    Parse FASTA file and extract sequence information.

    Args:
        fasta_path: Path to FASTA file

    Returns:
        List of sequence dictionaries
    """
    sequences = []

    try:
        for record in SeqIO.parse(fasta_path, "fasta"):
            seq_info = {
                'id': record.id,
                'description': record.description,
                'sequence_length': len(record.seq),
                'gc_content': calculate_gc_content(str(record.seq))
            }
            sequences.append(seq_info)

    except Exception as e:
        print(f"Error parsing FASTA: {e}")

    return sequences


def calculate_gc_content(sequence: str) -> float:
    """
    Calculate GC content of a DNA sequence.

    Args:
        sequence: DNA sequence string

    Returns:
        GC content as percentage
    """
    sequence = sequence.upper()
    gc_count = sequence.count('G') + sequence.count('C')
    total = len(sequence)

    if total == 0:
        return 0.0

    return (gc_count / total) * 100


def filter_variants_by_region(variants: List[Dict], chromosome: str,
                              start: int, end: int) -> List[Dict]:
    """
    Filter variants by genomic region.

    Args:
        variants: List of variant dictionaries
        chromosome: Chromosome name
        start: Start position
        end: End position

    Returns:
        Filtered list of variants
    """
    filtered = []

    for variant in variants:
        if (variant['chromosome'] == chromosome and
            start <= variant['position'] <= end):
            filtered.append(variant)

    return filtered


def annotate_variant_type(ref: str, alt: str) -> str:
    """
    Determine variant type based on reference and alternate alleles.

    Args:
        ref: Reference allele
        alt: Alternate allele

    Returns:
        Variant type string
    """
    if len(ref) == len(alt) == 1:
        return "SNV"  # Single Nucleotide Variant
    elif len(ref) < len(alt):
        return "INS"  # Insertion
    elif len(ref) > len(alt):
        return "DEL"  # Deletion
    else:
        return "COMPLEX"


def get_variant_summary(variants: List[Dict]) -> Dict:
    """
    Generate summary statistics for variants.

    Args:
        variants: List of variant dictionaries

    Returns:
        Summary statistics dictionary
    """
    summary = {
        'total_variants': len(variants),
        'by_chromosome': ,
        'by_type': {'SNV': 0, 'INS': 0, 'DEL': 0, 'COMPLEX': 0},
        'quality_stats': {
            'mean': 0,
            'min': float('inf'),
            'max': 0
        }
    }

    qualities = []

    for variant in variants:
        # Count by chromosome
        chrom = variant['chromosome']
        if chrom not in summary['by_chromosome']:
            summary['by_chromosome'][chrom] = 0
        summary['by_chromosome'][chrom] += 1

        # Count by type
        if variant['alternate']:
            var_type = annotate_variant_type(variant['reference'], variant['alternate'][0])
            summary['by_type'][var_type] += 1

        # Collect quality scores
        if variant['quality'] is not None:
            qualities.append(variant['quality'])

    # Calculate quality statistics
    if qualities:
        summary['quality_stats']['mean'] = sum(qualities) / len(qualities)
        summary['quality_stats']['min'] = min(qualities)
        summary['quality_stats']['max'] = max(qualities)

    return summary


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python genomics_utils.py <vcf_or_bam_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    path = Path(file_path)

    if not path.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    if file_path.endswith('.vcf') or file_path.endswith('.vcf.gz'):
        print("Parsing VCF file...")
        variants = parse_vcf_file(file_path)
        print(f"\nFound {len(variants)} variants")

        if variants:
            summary = get_variant_summary(variants)
            print("\nVariant Summary:")
            print(json.dumps(summary, indent=2))

    elif file_path.endswith('.bam'):
        print("Analyzing BAM file...")
        stats = get_bam_statistics(file_path)
        print("\nBAM Statistics:")
        print(json.dumps(stats, indent=2))

    elif file_path.endswith('.fasta') or file_path.endswith('.fa'):
        print("Parsing FASTA file...")
        sequences = parse_fasta_file(file_path)
        print(f"\nFound {len(sequences)} sequences")
        print(json.dumps(sequences, indent=2))
