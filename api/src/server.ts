import express from 'express';
import cors from 'cors';
import { runStylometryAnalysis } from './routes/stylo.ts'

const app = express();
app.use(cors());
app.use(express.json());

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.post('/api/stylometry', (req, res) => {
  const body = req.body;
  const controlText = body.controlText;
  const comparisonTexts = body.comparisonTexts;
  const analysisType = body.analysisType;
  const n = body.n || 1;
  let output;
  if (!!controlText && comparisonTexts.length > 0) {
    output = runStylometryAnalysis({
      controlText,
      comparisonTexts,
      analysisType,
      n,
    });
  }
  console.log("output:", output);
  res.json({ 
    status: 'ok',
    data: output,
 });
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => console.log(`API running on port ${PORT}`));