// TODO(efregoso): make common/utils/types.ts a standalone module to type analysisType
// import { StylometryAnalysisType } from '../../../common/utils/types';

interface StylometryOutput {
    comparisonScores: number[];
    weightedComparisonScores: number[];
}

export function runStylometryAnalysis(data: {
    controlText: string,
    comparisonTexts: string[],
    analysisType: string,
    n?: number,
}): StylometryOutput{
    let comparisonScores = [];
    let weightedComparisonScores = [];
    switch (data.analysisType) {
        case 'keyword': {
            const controlTable = createWordHashtable(data.controlText);
            for (const text of data.comparisonTexts) {
                const comparisonTable = createWordHashtable(text);
                comparisonScores.push(tallyScore({ 
                    control: controlTable, 
                    comparer: comparisonTable,
                }));
                weightedComparisonScores.push(tallyWeightedScore({
                    control: controlTable,
                    comparer: comparisonTable,
                }));
            }
            break;
        }
        case 'n-gram': {
            const controlTable = createNgramHashtable({ text: data.controlText, n: data.n || 1 });
            for (const text of data.comparisonTexts) {
                const comparisonTable = createNgramHashtable({ text, n: data.n || 1 });
                comparisonScores.push(tallyScore({
                    control: controlTable,
                    comparer: comparisonTable,
                }));
                weightedComparisonScores.push(tallyWeightedScore({
                    control: controlTable,
                    comparer: comparisonTable,
                }));
            }
            break;
        }
        default: {
            break;
        }
    }
    return {
        comparisonScores,
        weightedComparisonScores,
    };
}

function createWordHashtable(text: string): Map<string, number> {
    const hash = new Map<string, number>();
    if (!text) { return hash; }
    const textWords = text.split(" ");
    // TODO(efregoso): Check for alphanumeric -- exclude punctuation
    for (const word of textWords) {
        const lowercaseWord = word.toLowerCase();
        if (hash.has(lowercaseWord)) {
            hash.set(lowercaseWord, (hash.get(lowercaseWord) || 0) + 1);
        } else {
            hash.set(lowercaseWord, 1);
        }
    }
    return hash;
}

function createNgramHashtable(data: {
    text: string,
    n: number,
}): Map<string, number> {
    let hash = new Map<string, number>();
    if (!data.text) return hash;

    let i = 0;
    while (i + data.n - 1 < data.text.length) {
        let ngram = "";
        // Create an n gram from n letters
        for (let j = 0; j < data.n; j++) {
            ngram += data.text[i + j]?.toLowerCase();
        }
        if (!hash.has(ngram) && !!ngram) {
            hash.set(ngram, 1);
        } else if (hash.has(ngram)) {
            hash.set(ngram, (hash.get(ngram) || 0) + 1);
        }
        i++;
    }
    return hash;
}

function tallyScore(data: {
    control: Map<string, number>, 
    comparer: Map<string, number>
}): number {
    let score = 0;
    const keys = data.comparer.keys();
    for (const key of keys) {
        if (data.control.has(key)) {
            score = score + ((data.control.get(key) || 0) * (data.comparer.get(key) || 0));
        }
    }
    return score;
}

function tallyWeightedScore(data: {
    control: Map<string, number>, 
    comparer: Map<string, number>
}): number {
    let score = 0;
    const keys = data.comparer.keys();
    for (const key of keys) {
        if (data.comparer.has(key)) {
            let freqCtrl = data.control.get(key) || 0;
            let freqComp = data.comparer.get(key) || 0;
            if (freqComp >= 0.80 * freqCtrl && freqComp <= 1.20 * freqCtrl) {
                if (freqComp > 0.95 * freqCtrl && freqComp < 1.05 * freqCtrl) {
                    score += 2;
                }
            } else {
                score += 1;
            }
        }
    }
    return score;
}