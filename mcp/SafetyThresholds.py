class PolishThresholds:
    levels = [
        (2, 'zielony'),
        (10, 'źółty'),
        (25, 'czerwony'),
        (70, 'czarny'),
    ]

    def get_level(self, estimator_value):
        idx = 0
        for i, level in enumerate(self.levels):
            if estimator_value > level[0]:
                idx = i
            if estimator_value < level[0]:
                break
        return self.levels[idx]
