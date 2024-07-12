//import the file reader crate
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

//let's implement the file reading function

fn word_finder(file_path: &str, target_word: &str) -> io::Result<()> {
    let path = Path::new(file_path);

    let file = File::open(&path)?;
    //let's make a vector which will hold all the words.
    let reader = io::BufReader::new(file);
    let mut number_of_words = Vec::new();

    // just in each iteration, increment the number and print on each occurances.

    let mut line_num: i32 = 0; // we can use u32 also. i means signed and u is unsigned

    //iterate over all the lines
    for line in reader.lines() {
        line_num += 1;
        let line = line?;

        let mut col_num: i32 = 0; //same with col also
        for word in line.split_whitespace() {
            //remove the alphanumerics
            let word: String = word
                .chars()
                .filter(|c| c.is_ascii_alphanumeric())
                .collect::<String>()
                .to_lowercase();

            col_num += 1;
            if word == target_word {
                //push the words in the vector.
                number_of_words.push((line_num, col_num, word.to_string())); 
            }
        }
    }
    //iterating over the contents of the vector
    for (line_num, col_num, word) in number_of_words {
        println!("{} -> at {}:{}", word, line_num, col_num);
    }
    Ok(())
}

fn main() {
    let file_path = "test.txt";
    let target_word = "okay";

    if let Err(err) = word_finder(file_path, target_word) {
        eprintln!("Error searching for word: {}", err);
    }
}
