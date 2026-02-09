export function filterOutliersIQR(data: any[], values: number[][]) {
  // 1. Create index pairs and sort based on the values array
  const indexedData = data.map((obj, index) => ({ obj, index }));
  indexedData.sort((a, b) => {
    return Math.min(...values[a.index]) - Math.min(...values[b.index]);
  });

  // 2. Calculate Q1 (25th percentile) and Q3 (75th percentile) using all values
  const allValues = indexedData.flatMap(({ index }) => values[index]);
  const q1 = quantile(allValues, 0.25);
  const q3 = quantile(allValues, 0.75);

  // 3. Calculate IQR
  const iqr = q3 - q1;

  // 4. Define bounds
  const lowerBound = q1 - 1.5 * iqr;
  const upperBound = q3 + 1.5 * iqr;

  // 5. Filter the data
  return data.filter((_, index) => {
    const objValues = values[index];
    return objValues.every(
      (value) => value >= lowerBound && value <= upperBound
    );
  });
}

// Helper function to calculate percentiles
export function quantile(sortedArr: any[], q: number) {
  const pos = (sortedArr.length - 1) * q;
  const base = Math.floor(pos);
  const rest = pos - base;
  if (sortedArr[base + 1] !== undefined) {
    return sortedArr[base] + rest * (sortedArr[base + 1] - sortedArr[base]);
  }
  return sortedArr[base];
}
