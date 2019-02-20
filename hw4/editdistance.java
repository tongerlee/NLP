import java.io.*;
import java.util.*;

public class editdistance {

	public static void main(String[] args) {
		// javac editdistance.java
		// java editdistance 1 raw.txt dictionary.txt output1.txt
		// args[0] = 1
		// args[1] = raw.txt
		// args[2] = dictionary.txt
		// args[3] = output1.txt or output2.txt


		// Task 1
		File rawFile = new File(args[1]);
		File dictFile = new File(args[2]);
		File outputFile = new File(args[3]);
		// First, get all the raw words and store them into an arraylist.
		List<String> dictWords = new ArrayList<String>();
		String currDictWord;
		try {
			BufferedReader dictBR = new BufferedReader(
					new FileReader(dictFile));
			while((currDictWord = dictBR.readLine())!= null) {
				dictWords.add(currDictWord);
			}
			dictBR.close();
		} catch (IOException e1) {
			e1.printStackTrace();
		}


		// Then, start to iterate through the dictionary and calculate the Levenshtein distance
		try {
			int count = 0;
			BufferedReader rawBR = new BufferedReader(
					new FileReader(rawFile));
			BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile));
			String currWord;
			int minDistance = Integer.MAX_VALUE;
			String closestDictWord = "NONONO";
			while((currWord = rawBR.readLine()) != null) {
				minDistance = Integer.MAX_VALUE;
				closestDictWord = "NONONO";
				for(String currDict : dictWords) {
					// System.out.println(currRaw);
					int currDistance = Integer.MAX_VALUE;
					if(Integer.parseInt(args[0]) == 1) {
						currDistance = minEditDistance(currWord, currDict);
					} else if (Integer.parseInt(args[0]) == 2){
						currDistance = minEditDistanceWithTransposition(currWord, currDict);
					} else if (Integer.parseInt(args[0]) == 3) {
						currDistance = minEditDistanceWithDL(currWord, currDict);
					}
					if(currDistance < minDistance) {
						closestDictWord = currDict;
						minDistance = currDistance;
						System.out.println("Now minimum distance is " + minDistance + " for " + currWord);
					}
					if(minDistance == 0) {
						break;
					}
				}
				writer.write(closestDictWord + " " + minDistance + "\n");
				System.out.println("Done " + count++);
			}
			rawBR.close();
			writer.close();
		} catch (IOException e) {
			e.printStackTrace();
		}


	}

	public static int minEditDistance(String currWord, String currDict) {
		int m = currWord.length(); // source word
		int n = currDict.length(); // target word
		int[][] distance = new int[n+1][m+1];
		distance[0][0] = 0;
		for (int i = 0; i < n+1; i++) {
			for (int j = 0; j < m+1; j++) {
				if(i == 0) {
					distance[i][j] = j;
				} else if (j == 0) {
					distance[i][j] = i;
				} else if (currDict.charAt(i-1) == currWord.charAt(j-1)) {
					distance[i][j] = distance[i-1][j-1];
				} else {
					distance[i][j] = 1 + Math.min(distance[i][j-1], Math.min(distance[i-1][j], distance[i-1][j-1]));
				}
			}
		}

		return distance[n][m];	
	}

	public static int minEditDistanceWithTransposition(String currWord, String currDict) {
		int m = currWord.length(); // source word
		int n = currDict.length(); // target word
		int[][] distance = new int[n+1][m+1];
		distance[0][0] = 0;
		int cost = 0;
		for (int i = 0; i < n+1; i++) {
			for (int j = 0; j < m+1; j++) {
				cost = 0;
				if(i == 0) {
					distance[i][j] = j;
				} else if (j == 0) {
					distance[i][j] = i;
				} else if (currDict.charAt(i-1) == currWord.charAt(j-1)) {
					cost = 0;
					distance[i][j] = distance[i-1][j-1];
				} else {
					cost = 1;
					distance[i][j] = 1 + Math.min(distance[i][j-1], Math.min(distance[i-1][j], distance[i-1][j-1]));
				}
				if(i > 1 && j > 1) {
					if(currDict.charAt(i-1) == currWord.charAt(j-2) && currDict.charAt(i-2) == currWord.charAt(j-1)) {
						distance[i][j] = Math.min(distance[i][j], distance[i-2][j-2] + cost);
					}
				}
			}
		}

		return distance[n][m];	
	}

	public static int minEditDistanceWithDL(String currWord, String currDict) {
		int m = currWord.length(); // source word
		int n = currDict.length(); // target word
		int[][] distance = new int[n+2][m+2];
		int maxDistance = m+n;
		distance[0][0] = maxDistance;
		SortedMap<String, Integer> alphabet = new TreeMap<String, Integer>();
		for(String eachLetter : (currWord + currDict).split("")) {
			if(!alphabet.containsKey(eachLetter)){
				alphabet.put(eachLetter, 0);
			}
		}
		for (int i = 0; i < n; i++) {
			distance[i+1][0] = maxDistance;
			distance[i+1][1] = i;
		}
		for (int j = 0; j < m; j++) {
			distance[0][j+1] = maxDistance;
			distance[1][j+1] = j;
		}
		int cost = 0;
		for (int i = 1; i < n+1; i++) {
			int sub = 0;
			for (int j = 1; j < m+1; j++) {
				cost = 0;
				int subI = alphabet.get(currWord.split("")[j-1]);
				int subJ = sub;
				if (currDict.charAt(i-1) == currWord.charAt(j-1)) {
					cost = 0;
					sub = j;
					distance[i+1][j+1] = distance[i][j];
				} else {
					cost = 1;
					distance[i+1][j+1] = 1 + Math.min(distance[i][j], Math.min(distance[i][j+1], distance[i+1][j]));
				}

				distance[i+1][j+1] = Math.min(distance[i+1][j+1], distance[subI][subJ] + (i-subI-1) + 1 +(j-subJ-1));
			}
			alphabet.put(currDict.split("")[i-1], i);
		}

		return distance[n][m];	
	}

}
