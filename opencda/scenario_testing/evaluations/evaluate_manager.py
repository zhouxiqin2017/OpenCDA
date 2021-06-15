# -*- coding: utf-8 -*-
"""
Evaluation manager.
"""

# Author: Runsheng Xu <rxx3386@ucla.edu>
# License: MIT

import os
import sys
from datetime import datetime

import matplotlib.pyplot as plt

from opencda.scenario_testing.evaluations.utils import lprint


class EvaluationManager(object):
    """Evaluation manager to manage the analysis of the results for different modules.
    """

    def __init__(self, cav_world):
        """
        Construct class
        Args:
            cav_world (opencda.CavWorld): The CavWorld object that contains all CAVs' information
        """
        self.cav_world = cav_world

        current_path = os.path.dirname(os.path.realpath(__file__))
        current_time = datetime.now()
        # we create a folder for every single simulation based on the current time
        current_time = current_time.strftime("_%Y_%m_%d_%H_%M_%S")

        self.eval_save_path = os.path.join(current_path, '../../../evaluation_outputs', current_time)
        if not os.path.exists(self.eval_save_path):
            os.makedirs(self.eval_save_path)

    def evaluate(self):
        """
        Evaluate performance of all modules by plotting and writing the statistics into the log file.
        Returns:

        """
        log_file = os.path.join(self.eval_save_path, 'log.txt')

        self.localization_eval(log_file)
        print('Localization Evaluation Done.')

    def localization_eval(self, log_file):
        """
        Localization module evaluation.
        Args:
            log_file (File): The log file to write the data.

        Returns:

        """
        lprint(log_file, "***********Localization Module***********")
        for vid, vm in self.cav_world.get_vehicle_managers().items():
            actor_id = vm.vehicle.id
            lprint(log_file, 'Actor ID: %d' % actor_id)

            loc_debug_helper = vm.localizer.debug_helper
            figure, perform_txt = loc_debug_helper.evaluate()

            # save plotting
            figure_save_path = os.path.join(self.eval_save_path, '%d_localization_plotting.png' % actor_id)
            figure.savefig(figure_save_path, dpi=100)

            # save log txt
            lprint(log_file, perform_txt)
