'use client';

import { useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import FormControl from '@mui/material/FormControl';
import RadioGroup from '@mui/material/RadioGroup';
import Radio from '@mui/material/Radio';
import FormControlLabel from '@mui/material/FormControlLabel';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { StylometryAnalysisType } from '../common/utils/types';
import './stylometry.css';


export default function StylometryPage() {
    const [controlText, setControlText] = useState('');
    const [comparisonTexts, setComparisonTexts] = useState(['']);
    const [analysisType, setAnalysisType] = useState<StylometryAnalysisType>(StylometryAnalysisType.KEYWORD);
    const [nValue, setNValue] = useState<number>(1);
    const [comparisonScores, setComparisonScores] = useState([]);
    const [weightedComparisonScores, setWeightedComparisonScores] = useState([]);

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
        comparisonTexts.forEach((comparisonText, i) => {
            if (i !== index) {
                newComparisonTexts.push(comparisonText);
            }
        });
        setComparisonTexts(newComparisonTexts);
    }

    const handleSubmit = async () => {
        // TODO(efregoso): Backend integration for stylometry analysis.
        const controller = new AbortController();
        const signal = controller.signal;
        await fetch('http://localhost:4000/api/stylometry', { 
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ controlText, comparisonTexts, analysisType, n: nValue}),
            signal,
        }).then((res) => {
            return res.json();
        }).then((data) => {
            setComparisonScores(data.data.comparisonScores);
            setWeightedComparisonScores(data.data.weightedComparisonScores);
        })
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
                        defaultValue={StylometryAnalysisType.KEYWORD}
                        name="stylometry-analysis-type-radio-group"
                        value={analysisType}
                        onChange={(e) => setAnalysisType(e.target.value as StylometryAnalysisType)}
                    >
                        <FormControlLabel value={StylometryAnalysisType.KEYWORD} control={<Radio />} label="Keyword" />
                        <FormControlLabel value={StylometryAnalysisType.NGRAM} control={<Radio />} label="N-gram" />
                    </RadioGroup>
                </FormControl>
                <Button variant="contained" onClick={handleSubmit}>
                    Submit
                </Button>
            </Stack>

            <TableContainer>
                <Table className="stylo-results-table" aria-label="Results of analysis">
                    <TableHead>
                        <TableRow>
                            <TableCell align="center">Comparison text</TableCell>
                            <TableCell align="center">Score against control</TableCell>
                            <TableCell align="center">Weighted score against control</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {comparisonScores.map((value, index) => (
                            <TableRow key={index}>
                                <TableCell align="center">{ index + 1 }</TableCell>
                                <TableCell align="center">{ value }</TableCell>
                                <TableCell align="center">{ weightedComparisonScores[index] }</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    );
}