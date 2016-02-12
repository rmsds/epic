"""This is a module that computes the island threshold.

It is a sanitized and memory efficient version of the SICER version, that
produces results similar to the second or third decimal. I have a less efficient
version that gives even closer results, but I figure that the computations are
very approximate (due to how they are implemented in the original) so I just use
the faster version.
"""

from __future__ import print_function

import logging
import sys

from numpy import log
from itertools import count
from scipy.stats import poisson
from math import log, factorial, pi, exp

from epic.utils.helper_functions import lru_cache
from epic.config.genomes import get_effective_genome_length
from epic.statistics.compute_values_needed_for_recurrence import (
    compute_enriched_threshold, compute_gap_factor, compute_boundary)
from epic.statistics.compute_score_threshold import compute_score_threshold

from epic.config.cache_settings import MEMORY


# @MEMORY.cache(verbose=0)
def compute_background_probabilities(total_chip_count, genome, window_size,
                                     gaps_allowed):

    effective_genome_length = get_effective_genome_length(genome)
    logging.debug(str(effective_genome_length) + "effective_genome_length")
    # move outside of function call

    average_window_readcount = total_chip_count * (
        window_size / float(effective_genome_length))
    logging.debug(str(window_size) + " window size")
    logging.debug(str(total_chip_count) + " total chip count")
    logging.debug(str(average_window_readcount) + "average_window_readcount")

    island_enriched_threshold = compute_enriched_threshold(
        average_window_readcount)
    logging.debug(str(island_enriched_threshold) + "island_enriched_threshold")

    gap_contribution = compute_gap_factor(
        island_enriched_threshold, gaps_allowed, average_window_readcount)
    logging.debug(str(gap_contribution) + "gap_contribution")

    boundary_contribution = compute_boundary(
        island_enriched_threshold, gaps_allowed, average_window_readcount)
    logging.debug(str(boundary_contribution) + "boundary_contribution")

    genome_length_in_bins = effective_genome_length / window_size

    score_threshold = compute_score_threshold(
        average_window_readcount, island_enriched_threshold, gap_contribution,
        boundary_contribution, genome_length_in_bins)

    return score_threshold, island_enriched_threshold, average_window_readcount
