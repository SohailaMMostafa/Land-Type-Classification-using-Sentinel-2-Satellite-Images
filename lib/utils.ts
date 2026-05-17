export function formatProbabilities(probs: Record<string, number>) {
  return Object.entries(probs)
    .sort(([, a], [, b]) => b - a)
    .reduce(
      (acc, [key, val]) => {
        acc[key] = parseFloat(val.toFixed(2))
        return acc
      },
      {} as Record<string, number>
    )
}

export const CLASS_NAMES = [
  'AnnualCrop',
  'Forest',
  'HerbaceousVegetation',
  'Highway',
  'Industrial',
  'Pasture',
  'PermanentCrop',
  'Residential',
  'River',
  'SeaLake',
]
