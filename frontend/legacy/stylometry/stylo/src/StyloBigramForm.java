import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;
import java.lang.*;
import java.io.*;
import java.lang.Character;
import java.applet.Applet;

public class StyloBigramForm extends Applet {

        private static Scanner sc = null;

        public static void main(String[] args) {
            //args is going to be 0-4 length

            Hashtable<String, Integer> ctrl = StyloBigramForm.createHashtableAlpha("morrissamechar.txt");
            Hashtable<String, Integer> samp1 = StyloBigramForm.createHashtableAlpha("keefauver2samechar.txt");
            Hashtable<String, Integer> samp2 = StyloBigramForm.createHashtableAlpha("mason2samechar.txt");
            Hashtable<String, Integer> samp3 = StyloBigramForm.createHashtableAlpha("monty2samechar.txt");
            //compare values with the first guy & tally "points": frequency is a weight variable
            Enumeration<String> e = ctrl.keys();
            System.out.println("Bigram score between control and Sample 1: " + tallyWeightedScore(ctrl, samp1, e));
            e = ctrl.keys();
            System.out.println("Bigram score between control and Sample 2: " + tallyWeightedScore(ctrl, samp2, e));
            e = ctrl.keys();
            System.out.println("Bigram score between control and Sample 3: " + tallyWeightedScore(ctrl, samp3, e));
            System.exit(0);
        }

        public static Hashtable<String, Integer> createHashtableAlpha(String filename) {
            Hashtable<String, Integer> hash = new Hashtable<String, Integer>();
            try {
                sc = new Scanner(new File("C:\\Users\\super\\Google Drive (emf65@case.edu)\\Code\\Git\\STYLO\\src\\DATA blog posts\\" + filename));
            } catch (FileNotFoundException e) {
                System.out.println("File not found: " + filename);
                System.exit(1);
            }
            for (; sc.hasNextLine(); ) {
                String line = sc.nextLine();
                line = line.toLowerCase();
                //create a character array
                char[] lineArray = line.toCharArray();
                StringBuilder amendWord = new StringBuilder();
                // remove everything that isn't an alphanumeric character
                for (int j = 0; j < lineArray.length; j++) {  //for each word in the line
                    if (Character.isLetter(lineArray[j]) || lineArray[j] == ' ') {
                        amendWord.append(lineArray[j]);
                    }
                }
                char[] newLine = amendWord.toString().toCharArray();
                //go through each pair of letters & add entries into the hashtable
                for (int k = 0; k+1 < newLine.length; k++) {
                    if (newLine[k] != ' ' && newLine[k+1] != ' ') {
                        StringBuilder buffer = new StringBuilder();
                        buffer.append(newLine[k]);
                        buffer.append(newLine[k + 1]);
                        String bigram = buffer.toString();
                        //if the hashtable does not have this bigram in it, add it
                        if (hash.containsKey(bigram) == false) {
                            hash.put(bigram, 1);
                        } else {
                            int newValue = hash.get(bigram);
                            newValue++;
                            hash.put(bigram, newValue);
                        }
                    }
                }
            }
            sc.close();
            System.out.println(hash.toString());
            return hash;
        }

        public static int tallyScore(Hashtable<String, Integer> control, Hashtable<String, Integer> comparer, Enumeration<String> e){
            int score = 0;
            for (; e.hasMoreElements();) {
                String compare = e.nextElement();
                if (comparer.containsKey(compare)){
                    score = score + (control.get(compare)*comparer.get(compare));
                }
            }
            return score;
        }

        public static int tallyWeightedScore(Hashtable<String, Integer> control, Hashtable<String, Integer> comparer, Enumeration<String> e){
            int score = 0;
            for (; e.hasMoreElements();) {
                String compare = e.nextElement();
                if (comparer.containsKey(compare)){
                    int freqctrl = control.get(compare);
                    int freqcomp = comparer.get(compare);
                    if (freqcomp >= 0.80*freqctrl && freqcomp <=1.20*freqctrl) {
                        if (freqcomp > 0.95*freqctrl && freqcomp < 1.05*freqctrl) {
                            score = score + 2;
                        }
                        else {
                            score = score + 1;
                        }
                    }
                }
            }
            return score;
        }

    }

}
