use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn word_finder(file_path: &str, target_word: &str) -> io::Result<()> {
    let path = Path::new(file_path);
    // Open the file
    let file = File::open(&path)?;
    let reader = io::BufReader::new(file);

    let mut number_of_words = Vec::new();

    let mut line_num: i32 = 0;
    // Iterate over lines in the file
    for line in reader.lines() {
        //dbg!(&line);
        line_num += 1;
        let line = line?;

        let mut col_num: i32 = 0;
        // Split the line into words and check each word
        for word in line.split_whitespace() {
            dbg!(&word);
            let word: String = word
                .chars()
                .filter(|c| c.is_ascii_alphanumeric())
                .collect::<String>()
                .to_lowercase();

            //dbg!(line.split_whitespace());
            col_num += 1;
            if word == target_word {
                number_of_words.push((line_num, col_num, word.to_string()));
                //println!("Found word: {} {}:{}", word, line_num, col_num);
            }
        }
    }
    dbg!(&number_of_words);
    for (line_num, col_num, word) in number_of_words {
        println!("{} {}:{}", word, line_num, col_num);
    }
    Ok(())
}

fn main() {
    //println!("Current working directory: {:?}", std::env::current_dir());
    let file_path = "test.txt"; //file path
    let target_word = "example"; // word to find

    if let Err(err) = word_finder(file_path, target_word) {
        eprintln!("Error searching for word: {}", err);
    }
}
