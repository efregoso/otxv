import { ORDERED_GLOSSARY_TERMS } from "./glossary_terms";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

import "./glossary.css";

export default function GlossaryPage() {

    return (
    <div id="main-body" className="">
        <h2>Glossary</h2>
        <TableContainer component={Paper}>
            <Table className="glossary-table">
                <TableHead>
                    <TableRow className="glossary-table-header-row">
                        <TableCell className="glossary-table-head-cell" align="center">
                            <b>Term</b>
                        </TableCell>
                        <TableCell className="glossary-table-head-cell" align="center">
                            <b>Definition</b>
                        </TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {ORDERED_GLOSSARY_TERMS.map((term) => (
                        <TableRow key={ term.word }>
                            <TableCell className="glossary-term">
                                <b>{ term.word }</b>
                            </TableCell>
                            <TableCell className="glossary-definition">{ term.meaning }</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    </div>
    );
}