import { ORDERED_GLOSSARY_TERMS } from "./glossary_terms";
import "./glossary.css";

export default function GlossaryPage() {

    return (
    <div id="main-body">
        <h1>Glossary</h1>
        <table className="glossary-table">
            <thead>
                <tr>
                    <th>Term</th>
                    <th>Definition</th>
                </tr>
            </thead>
            <tbody>
                {ORDERED_GLOSSARY_TERMS.map((term) => (
                    <tr key={term.word}>
                        <td className="glossary-term">{term.word}</td>
                        <td className="glossary-definition">{term.meaning}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
    );
}