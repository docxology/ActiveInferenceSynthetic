import matplotlib.pyplot as plt
import numpy as np

from src.demos import VOI_ACCURACIES, VOI_COST
from src.figures.decision_value import build_figure


def test_utility_curve_has_binary_analytic_reference_and_distinct_units():
    figure = build_figure()
    utility, information = figure.axes
    assert utility.get_ylabel() == "expected utility gain"
    assert information.get_ylabel() == "mutual information (nats)"
    np.testing.assert_allclose(utility.lines[0].get_ydata(), VOI_ACCURACIES - 0.5)
    np.testing.assert_allclose(utility.lines[1].get_ydata(), VOI_ACCURACIES - 0.5 - VOI_COST)
    np.testing.assert_allclose(utility.lines[2].get_ydata(), 0, atol=1e-15)
    assert information.lines[0].get_ydata()[-1] > 0
    plt.close(figure)
