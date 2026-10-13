"""Run: python -m unittest discover -s tests"""
import sys, unittest, random, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from netlib import rank, npmi
from decision_rule import analyse, sample_brand_indices

class AnalysisTests(unittest.TestCase):
    def test_average_ties_are_name_independent(self):
        self.assertEqual(rank({'B': 8, 'A': 8, 'C': 1}), {'A': 1.5, 'B': 1.5, 'C': 3.0})

    def test_ranking_populations_match_and_leaves_cannot_be_bridges(self):
        sets = [['A','B']]*5 + [['B','C']]*5 + [['Isolate']]*5 + [['Other']]*85
        a = analyse(sets, k=5, minf=5)
        self.assertEqual(set(a['br']), set(a['fr']))
        self.assertEqual(set(a['br']), {'A','B','C'})
        self.assertEqual(a['bridges'], {'B'})
        self.assertEqual(a['br']['A'], a['br']['C'])

    def test_whole_cluster_multiplicity_no_truncation(self):
        groups = {'large': list(range(10)), 'small': [10]}
        for seed in range(20):
            indices, selected = sample_brand_indices(groups, random.Random(seed))
            self.assertEqual(len(selected), len(groups))
            counts = collections.Counter(indices)
            for brand, members in groups.items():
                self.assertTrue(all(counts[i] == selected.count(brand) for i in members))

    def test_constant_pair_npmi_is_neutral(self):
        self.assertEqual(npmi(5, {'A':5,'B':5}, {('A','B'):5}, 'A','B'), 0.0)

if __name__ == '__main__': unittest.main()
