'use client';

import { useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import FormControl from '@mui/material/FormControl';
import RadioGroup from '@mui/material/RadioGroup';
import Radio from '@mui/material/Radio';
import FormControlLabel from '@mui/material/FormControlLabel';
import './stylometry.css';

enum AnalysisType {
    KEYWORD = 'keyword',
    NGRAM = 'n-gram',
}

export default function StylometryPage() {
    const [controlText, setControlText] = useState('');
    const [comparisonTexts, setComparisonTexts] = useState(['', '', '']);
    const [analysisType, setAnalysisType] = useState<AnalysisType>(AnalysisType.KEYWORD);

    const handleComparisonTextChange = (value: string, index: number) => {
        const newComparisonTexts = structuredClone(comparisonTexts);
        newComparisonTexts[index] = value;
        setComparisonTexts(newComparisonTexts);
    }

    const addComparisonText = () => {
        setComparisonTexts([...comparisonTexts, '']);
    }

    const removeComparisonText = (index: number) => {
        let newComparisonTexts: string[] = [];
        //newComparisonTexts.splice(index, 1);
        comparisonTexts.forEach((comparisonText, i) => {
            if (i !== index) {
                newComparisonTexts.push(comparisonText);
            }
        });
        setComparisonTexts(newComparisonTexts);
    }

    const handleSubmit = () => {
        // TODO(efregoso): Backend integration for stylometry analysis.
        console.log(`Submitted control text: ${controlText}`);
        console.log(`Comparison texts: ${comparisonTexts.join(', ')}`);
    };

    return (
        <div className="stylometry-content-container">
            <h1>STYLO: (Naive) Stylometric Text Analysis Tool</h1>
            <Stack className="stylometry-form-stack" direction="column" spacing={7}>
                <div className="stylometry-control-text-container">
                    <TextField
                        required
                        id="stylometry-control-text-input"
                        label="Control Text"
                        multiline={true}
                        minRows={10}
                        fullWidth={true}
                        value={controlText}
                        onChange={(e) => setControlText(e.target.value)}
                    />
                </div>
                {comparisonTexts.map((text, index) => (
                    <div className="stylometry-comparison-text-container" key={index}>
                        <TextField
                            required
                            className="stylometry-comparison-text-input"
                            id={`stylometry-comparison-text-input-${index}`}
                            label={`Comparison Text ${index + 1}`}
                            multiline={true}
                            minRows={10}
                            fullWidth={true}
                            value={text}
                            onChange={(e) => handleComparisonTextChange(e.target.value, index)}
                        />
                        <Button onClick={() => removeComparisonText(index)}>Remove Comparison Text</Button>
                    </div>
                ))}
                <Button variant="contained" onClick={addComparisonText}>
                    Add Comparison Text
                </Button>
                <FormControl>
                    <RadioGroup
                        aria-labelledby="stylometry-analysis-type"
                        defaultValue={AnalysisType.KEYWORD}
                        name="stylometry-analysis-type-radio-group"
                        value={analysisType}
                        onChange={(e) => setAnalysisType(e.target.value as AnalysisType)}
                    >
                        <FormControlLabel value={AnalysisType.KEYWORD} control={<Radio />} label="Keyword" />
                        <FormControlLabel value={AnalysisType.NGRAM} control={<Radio />} label="N-gram" />
                    </RadioGroup>
                </FormControl>
                <Button variant="contained" onClick={handleSubmit}>
                    Submit
                </Button>
            </Stack>
        </div>
    );
}