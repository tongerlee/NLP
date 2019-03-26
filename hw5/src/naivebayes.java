import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

public class naivebayes {

	public static void main(String[] args) {
		// args[0] is train
		// args[1] is test
		// args[2] is train2
		// args[3] is test2
		File train = new File(args[0]);
		File test = new File(args[1]);
		File task1 = new File("src\\task1.txt");
		try {
			BufferedWriter result = new BufferedWriter(new FileWriter(task1));

			helper(train, test, result);
			train = new File(args[2]);
			test = new File(args[3]);
			helper(train, test, result);
			result.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	 public static Map<String, Double> sortByValue(Map<String, Double> hm) 
	    { 
	        // Create a list from elements of HashMap 
	        List<Map.Entry<String, Double> > list = 
	               new LinkedList<Map.Entry<String, Double> >(hm.entrySet()); 
	  
	        // Sort the list 
	        Collections.sort(list, new Comparator<Map.Entry<String, Double> >() { 
	            public int compare(Map.Entry<String, Double> o1,  
	                               Map.Entry<String, Double> o2) 
	            { 
	                return (o2.getValue()).compareTo(o1.getValue()); 
	            } 
	        }); 
	          
	        // put data from sorted list to hashmap  
	        Map<String, Double> temp = new HashMap<String, Double>(); 
	        int count = 0;
	        for (Map.Entry<String, Double> aa : list) { 
	        	if(count == 0) {
	        		temp.put(aa.getKey(), aa.getValue()); 
	        	} else {
	        		count--;
	        	}
	        } 
	        return temp; 
	    }

	public static void helper(File train, File test, BufferedWriter result) {

		Map<String, Double> blueWords = new HashMap<String, Double>();
		Map<String, Double> blueBigrams = new HashMap<String, Double>();
		Map<String, Double> redWords = new HashMap<String, Double>();
		Map<String, Double> redBigrams = new HashMap<String, Double>();

		double sum_blueWords = 0.0;
		double sum_redWords = 0.0;
		double blue_count = 0.0;
		double red_count = 0.0;
		double vocabulary = 0.0;
		
		double sum_blueBigrams = 0.0;
		double sum_redBigrams = 0.0;
		try {
			Scanner trainsc = new Scanner(train);
			while(trainsc.hasNextLine()) {
				String curr_line = trainsc.nextLine();
				String[] curr_content_tmp = curr_line.split("\\t");
				String curr_class = curr_content_tmp[0];
				String[] curr_content = curr_content_tmp[1].split(" ");
				if(curr_class.equalsIgnoreCase("BLUE")) {
					blue_count++;
				} else {
					red_count++;
				}
				for(int i = 1; i < curr_content.length; i++) {
					String curr_word = curr_content[i].toLowerCase();
					if (!blueWords.containsKey(curr_word) 
							&& !redWords.containsKey(curr_word)) {
						vocabulary++;
					}
					if(curr_class.equalsIgnoreCase("BLUE")) {
						sum_blueWords++;
						if(blueWords.containsKey(curr_word)) {
							double oldvalue = blueWords.get(curr_word);
							blueWords.replace(curr_word, 
									(oldvalue+1.0));
						} else {
							blueWords.put(curr_word, 1.0);
						}
					} else {
						sum_redWords++;
						if(redWords.containsKey(curr_word)) {
							double oldvalue = redWords.get(curr_word);
							redWords.replace(curr_word, 
									(oldvalue+1.0));
						} else {
							redWords.put(curr_word, 1.0);
						}
					}
				}
				
				for(int i = 1; i < curr_content.length - 1; i++) {
					String curr_word = curr_content[i].toLowerCase();
					String next_word = curr_content[i+1].toLowerCase();
					if(curr_class.equalsIgnoreCase("BLUE")) {
						sum_blueBigrams++;
						if(blueBigrams.containsKey(curr_word + " " + next_word)) {
							double oldvalue = blueBigrams.get(curr_word + " " + next_word);
							blueBigrams.replace(curr_word + " " + next_word, 
									(oldvalue+1.0));
						} else {
							blueBigrams.put(curr_word + " " + next_word, 1.0);
						}
					} else {
						sum_redBigrams++;
						if(redBigrams.containsKey(curr_word + " " + next_word)) {
							double oldvalue = redBigrams.get(curr_word + " " + next_word);
							redBigrams.replace(curr_word + " " + next_word, 
									(oldvalue+1.0));
						} else {
							redBigrams.put(curr_word + " " + next_word, 1.0);
						}
					}
				}
			}
			trainsc.close();
		} catch (IOException e) {
			System.out.println("Error Openning Trainning File!");
			e.printStackTrace();
		}
		//		System.out.println(vocabulary);
		//		System.out.println(blueWords.size());
		//		System.out.println(redWords.size());
		//		System.out.println(sum_blueWords);
		blueWords = sortByValue(blueWords);
		System.out.println(blueWords.size());
		redWords = sortByValue(redWords);
		System.out.println(redWords.size());
//		sum_blueWords -= 500;
//		sum_redWords -= 500;
//		vocabulary -= 500;
		int reduce = 5;
		Map<String, Double> blueWords_new = new HashMap<String, Double>();
		for(Map.Entry<String, Double> eachEntry : blueWords.entrySet()) {
			if(reduce > 0 && redWords.containsKey(eachEntry.getKey())) {
				reduce--;
				redWords.remove(eachEntry.getKey());
				vocabulary -= 1;
				sum_blueWords -= 1;
				sum_redWords -= 1;
			} else {
				blueWords_new.put(eachEntry.getKey(), eachEntry.getValue());
			}
		}
		blueWords = blueWords_new;
		
		for(Map.Entry<String, Double> eachEntry : blueWords.entrySet()) {
			eachEntry.setValue((eachEntry.getValue() + 1.0) / 
					(sum_blueWords + vocabulary));
		}
		for(Map.Entry<String, Double> eachEntry : redWords.entrySet()) {
			eachEntry.setValue((eachEntry.getValue() + 1.0) / 
					(sum_redWords + vocabulary));
		}
		for(Map.Entry<String, Double> eachEntry : blueBigrams.entrySet()) {
			eachEntry.setValue((eachEntry.getValue() + 1.0) / 
					(sum_blueBigrams+ vocabulary));
		}
		for(Map.Entry<String, Double> eachEntry : redBigrams.entrySet()) {
			eachEntry.setValue((eachEntry.getValue() + 1.0) / 
					(sum_redBigrams + vocabulary));
		}
		
//		blueBigrams = sortByValue(blueBigrams);
//		System.out.println(blueBigrams.size());
//		redBigrams = sortByValue(redBigrams);
//		System.out.println(redBigrams.size());
		

		double prior_blue = blue_count / (blue_count + red_count);
		double prior_red = red_count / (blue_count + red_count);
		

		double log_prob_blue = Math.log(prior_blue);
		double log_prob_red = Math.log(prior_red);
		
		double log_prob_blue_bi = Math.log(prior_blue);
		double log_prob_red_bi = Math.log(prior_red);
		
		double correctness = 0.0;
		double corr_red = 0.0;
		double corr_blue = 0.0;
		double false_red = 0.0;
		double false_blue = 0.0;
		double count = 0.0;
		double unseen_blue = 1.0 / (sum_blueWords + vocabulary);
		double unseen_red = 1.0 / (sum_redWords + vocabulary);
		
		double unseen_blue_bi = 1.0 / (sum_blueBigrams + vocabulary);
		double unseen_red_bi = 1.0 / (sum_redBigrams + vocabulary);
		
		double correctness_bi = 0.0;
		double corr_red_bi = 0.0;
		double corr_blue_bi = 0.0;
		double false_red_bi = 0.0;
		double false_blue_bi = 0.0;
		
		try {
			Scanner testsc = new Scanner(test);
			while(testsc.hasNextLine()) {
				count++;
				String curr_line_test = testsc.nextLine();
				String[] curr_content_tmp_test = curr_line_test.split("\\t");
				String curr_class_test = curr_content_tmp_test[0];
				String[] curr_content_test = curr_content_tmp_test[1].split(" ");
				log_prob_blue = Math.log(prior_blue);
				log_prob_red = Math.log(prior_red);
				
				log_prob_blue_bi = Math.log(prior_blue);
				log_prob_red_bi = Math.log(prior_red);
				
				for(int i = 1; i < curr_content_test.length; i++) {
					String curr_word = curr_content_test[i].toLowerCase();
					curr_word = curr_word.toLowerCase();
					// Blue
					if(blueWords.containsKey(curr_word)) {
						log_prob_blue += Math.log(blueWords.get(curr_word));
					} else {
						log_prob_blue += Math.log(unseen_blue);
					} 
					// Red
					if(redWords.containsKey(curr_word)) {
						log_prob_red += Math.log(redWords.get(curr_word));
					} else {
						log_prob_red += Math.log(unseen_red);
					}
				}
				
				for(int i = 1; i < curr_content_test.length - 1; i++) {
					String curr_word = curr_content_test[i].toLowerCase();
					String next_word = curr_content_test[i+1].toLowerCase();					
					// Blue
					if(blueBigrams.containsKey(curr_word + " " + next_word)) {
						log_prob_blue_bi += Math.log(blueBigrams.get(curr_word + " " + next_word));
					} else {
						log_prob_blue_bi += Math.log(unseen_blue_bi);
					} 
					// Red
					if(redBigrams.containsKey(curr_word + " " + next_word)) {
						log_prob_red_bi += Math.log(redBigrams.get(curr_word + " " + next_word));
					} else {
						log_prob_red_bi += Math.log(unseen_red_bi);
					}
				}
				// System.out.println("Test Speech [" + count + "] " + "(" + curr_class_test + "): Blue Prob = " + String.format("%.4f",log_prob_blue) + " , Red Prob = " + String.format("%.4f\n",log_prob_red));
				if(log_prob_blue >= log_prob_red) {
					if(curr_class_test.equalsIgnoreCase("BLUE")) {
						correctness++;
						corr_blue++;
					} else {
						false_blue++;
						System.out.println("Test Speech [" + count + "] (" + curr_class_test + ") was predicted wrong");
					}
					// System.out.println("C");
				} else {
					if(curr_class_test.equalsIgnoreCase("RED")) {
						correctness++;
						corr_red++;
					} else {
						false_red++;
						System.out.println("Test Speech [" + count + "] " + "(" + curr_class_test + ") was predicted wrong\n");
					}
					// System.out.println("L");
				}
				
				if(log_prob_blue_bi >= log_prob_red_bi) {
					if(curr_class_test.equalsIgnoreCase("BLUE")) {
						correctness_bi++;
						corr_blue_bi++;
					} else {
						false_blue_bi++;
						System.out.println("Test Speech [" + count + "] (" + curr_class_test + ") was predicted wrong in bigrams");
					}
					// System.out.println("C");
				} else {
					if(curr_class_test.equalsIgnoreCase("RED")) {
						correctness_bi++;
						corr_red_bi++;
					} else {
						false_red_bi++;
						System.out.println("Test Speech [" + count + "] " + "(" + curr_class_test + ") was predicted wrong in bigrams\n");
					}
					// System.out.println("L");
				}
				System.out.println("Test Speech [" + count + "] " + "(" + curr_class_test + "): Blue Prob = " + String.format("%.4f",log_prob_blue_bi) + " , Red Prob = " + String.format("%.4f\n",log_prob_red_bi));
			}
//			result.write("overall accuracy\n" + String.format("%.4f\n", (correctness / count)));
//			result.write("precision for red\n"+ String.format("%.4f\n", (corr_red / (corr_red + false_red))));
//			result.write("recall for red\n"+ String.format("%.4f\n", (corr_red / (corr_red + false_blue))));
//			result.write("precision for blue\n"+ String.format("%.4f\n", (corr_blue / (corr_blue + false_blue))));
//			result.write("recall for blue\n"+ String.format("%.4f\n\n", (corr_blue / (corr_blue + false_red))));

			System.out.println("overall accuracy\n" + String.format("%.4f\n", (correctness / count)));
			System.out.println("precision for red\n"+ String.format("%.4f\n", (corr_red / (corr_red + false_red))));
			System.out.println("recall for red\n"+ String.format("%.4f\n", (corr_red / (corr_red + false_blue))));
			System.out.println("precision for blue\n"+ String.format("%.4f\n", (corr_blue / (corr_blue + false_blue))));
			System.out.println("recall for blue\n"+ String.format("%.4f\n\n", (corr_blue / (corr_blue + false_red))));
			
			
			System.out.print("-------------------------------------------Bigrams result below----------------------------------------\n");
			System.out.println("overall accuracy\n" + String.format("%.4f\n", (correctness_bi / count)));
			System.out.println("precision for red\n"+ String.format("%.4f\n", (corr_red_bi / (corr_red_bi + false_red_bi))));
			System.out.println("recall for red\n"+ String.format("%.4f\n", (corr_red_bi / (corr_red_bi + false_blue_bi))));
			System.out.println("precision for blue\n"+ String.format("%.4f\n", (corr_blue_bi / (corr_blue_bi + false_blue_bi))));
			System.out.println("recall for blue\n"+ String.format("%.4f\n\n", (corr_blue_bi / (corr_blue_bi + false_red_bi))));
			System.out.println(sum_redBigrams);
			System.out.println(sum_redWords);
			testsc.close();
		} catch (IOException e) {
			System.out.println("Error Openning Test File!");
			e.printStackTrace();
		}
	}

}
