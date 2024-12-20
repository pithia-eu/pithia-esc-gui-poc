export function checkForSimilarSourceNames(sourceNames) {
    return Array.from(sourceNames).reduce((accumulator, sourceName) => {
        const sourceNameNormalised = _.kebabCase(sourceName);
        if (!(sourceNameNormalised in accumulator)) {
            accumulator[sourceNameNormalised] = [];
        }
        accumulator[sourceNameNormalised].push(sourceName);
        return accumulator;
    }, {});
}