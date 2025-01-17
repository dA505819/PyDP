import numpy as np
import pytest
from pydp.algorithms.partition_selection import create_partition_strategy

N_SIMULATIONS = 100000
ACCURACY_THRESHOLD = 1e-1


class TestPartitionSelection:
    @pytest.mark.parametrize(
        [
            "num_users",
            "epsilon",
            "delta",
            "max_partitions_contributed",
            "expected_prob",
        ],
        [
            (10, 1, 1e-5, 1, 0.12818308050524607),
            (700, 0.2, 1e-7, 10, 0.5800625857189882),
        ],
    )
    def test_truncated_geometric(
        self, num_users, epsilon, delta, max_partitions_contributed, expected_prob
    ):
        partition_selector = create_partition_strategy(
            "truncated_geometric", epsilon, delta, max_partitions_contributed
        )
        assert epsilon == partition_selector.epsilon
        assert delta == partition_selector.delta
        assert (
            max_partitions_contributed == partition_selector.max_partitions_contributed
        )
        prob_of_keep = partition_selector.probability_of_keep(num_users)
        assert prob_of_keep == pytest.approx(expected_prob)

        sims = [partition_selector.should_keep(num_users) for _ in range(N_SIMULATIONS)]
        pred_prob_of_keep = np.mean(sims)
        assert pred_prob_of_keep == pytest.approx(expected_prob, ACCURACY_THRESHOLD)

    @pytest.mark.parametrize(
        [
            "num_users",
            "epsilon",
            "delta",
            "max_partitions_contributed",
            "expected_prob",
        ],
        [
            (10, 1, 1e-5, 1, 0.08103083927575383),
            (700, 0.2, 1e-7, 10, 0.011787911768969317),
        ],
    )
    def test_laplace_keep_and_return_noised_value(
        self, num_users, epsilon, delta, max_partitions_contributed, expected_prob
    ):
        partition_selector = create_partition_strategy(
            "laplace", epsilon, delta, max_partitions_contributed
        )
        assert epsilon == partition_selector.epsilon
        assert delta == partition_selector.delta
        assert (
            max_partitions_contributed == partition_selector.max_partitions_contributed
        )
        prob_of_keep = partition_selector.probability_of_keep(num_users)
        assert prob_of_keep == pytest.approx(expected_prob)

        sims = [partition_selector.should_keep(num_users) for _ in range(N_SIMULATIONS)]
        pred_prob_of_keep = np.mean(sims)
        assert pred_prob_of_keep == pytest.approx(expected_prob, ACCURACY_THRESHOLD)

        noised_values = [
            partition_selector.noised_value_if_should_keep(num_users)
            for _ in range(N_SIMULATIONS)
        ]
        noised_values = [v for v in noised_values if v]
        assert len(noised_values) / N_SIMULATIONS == pytest.approx(
            expected_prob, ACCURACY_THRESHOLD
        )
        assert all([(v >= partition_selector.threshold) for v in noised_values])

    @pytest.mark.parametrize(
        [
            "num_users",
            "epsilon",
            "delta",
            "max_partitions_contributed",
            "expected_prob",
        ],
        [
            (10, 1, 1e-5, 1, 0.017845473615190732),
            (1100, 0.2, 1e-7, 10, 0.007884076914531857),
        ],
    )
    def test_gaussian_keep_and_return_noised_value(
        self, num_users, epsilon, delta, max_partitions_contributed, expected_prob
    ):
        partition_selector = create_partition_strategy(
            "gaussian", epsilon, delta, max_partitions_contributed
        )
        assert epsilon == partition_selector.epsilon
        assert delta == partition_selector.delta
        assert (
            max_partitions_contributed == partition_selector.max_partitions_contributed
        )
        prob_of_keep = partition_selector.probability_of_keep(num_users)
        assert prob_of_keep == pytest.approx(expected_prob)

        sims = [partition_selector.should_keep(num_users) for _ in range(N_SIMULATIONS)]
        pred_prob_of_keep = np.mean(sims)
        assert pred_prob_of_keep == pytest.approx(expected_prob, ACCURACY_THRESHOLD)

        noised_values = [
            partition_selector.noised_value_if_should_keep(num_users)
            for _ in range(N_SIMULATIONS)
        ]
        noised_values = [v for v in noised_values if v]
        assert len(noised_values) / N_SIMULATIONS == pytest.approx(
            expected_prob, ACCURACY_THRESHOLD
        )
        assert all([(v >= partition_selector.threshold) for v in noised_values])
