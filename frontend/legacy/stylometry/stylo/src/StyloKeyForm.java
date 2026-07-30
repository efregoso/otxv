import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;
import java.lang.*;
import java.io.*;
import java.lang.Character;

public class StyloKeyForm extends Applet {

    private static Scanner sc = null;

    public static void main(String[] args) {
        Hashtable<String, Integer> ctrl = StyloKeyForm.createHashtableAlpha("alistairsameword.txt");
        Hashtable<String, Integer> samp1 = StyloKeyForm.createHashtableAlpha("keefauver2sameword.txt");
        Hashtable<String, Integer> samp2 = StyloKeyForm.createHashtableAlpha("mason2sameword.txt");
        Hashtable<String, Integer> samp3 = StyloKeyForm.createHashtableAlpha("monty2sameword.txt");
        //compare values with the first guy & tally "points": frequency is a weight variable
        //(freq1alistair * freq1other) + (freq2alistair * freq2other) + ..
        Enumeration<String> e = ctrl.keys();
        System.out.println("Keyword score between control and Sample 1: " + tallyWeightedScore(ctrl, samp1, e));
        e = ctrl.keys();
        System.out.println("Keyword score between control and Sample 2: " + tallyWeightedScore(ctrl, samp2, e));
        e = ctrl.keys();
        System.out.println("Keyword score between control and Sample 3: " + tallyWeightedScore(ctrl, samp3, e));
        e = ctrl.keys();
        System.exit(0);
    }

    public static Hashtable<String, Integer> createHashtableAlpha(String filename) {
        Hashtable<String, Integer> hash = new Hashtable<String, Integer>();
        try {
            sc = new Scanner(new File("C:\\Users\\super\\Google Drive (emf65@case.edu)\\Code\\Git\\STYLO\\src\\DATA blog posts\\" + filename));
        } catch (FileNotFoundException e) {
            System.out.println("File not found.");
            System.exit(1);
        }
        for (; sc.hasNextLine(); ) {
            String line = sc.nextLine();
            //split line along spaces
            String[] lineArray = line.split(" ");
            // remove everything that isn't an alphanumeric character
            for (int j = 0; j < lineArray.length; j++) {  //for each word in the line
                String word = lineArray[j];
                StringBuilder amendWord = new StringBuilder();
                for (int k = 0; k < word.length(); k++) {    //for each letter in the word
                    if (Character.isLetter(word.charAt(k))) {
                        amendWord.append(word.charAt(k));
                    }
                }
                word = amendWord.toString();
                word = word.toLowerCase();
                //if the hashtable does not have this word in it, add it
                if (hash.containsKey(word) == false && word.length() >= 5) {
                    hash.put(word, 1);
                } else if (word.length() >= 5) {
                    int newValue = hash.get(word);
                    newValue++;
                    hash.put(word, newValue);
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
                int diff = Math.abs(freqctrl - freqcomp);
                if (freqcomp >= 0.75*freqctrl && freqcomp <=1.25*freqctrl) {
                    if (freqcomp > 0.9*freqctrl && freqcomp < 1.1*freqctrl) {
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
