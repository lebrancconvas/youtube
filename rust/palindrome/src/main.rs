use std::io;
use std::io::Write;

fn is_palindrome(s: &str) -> bool {
    // Convert the input string to lowercase and filter out non-alphanumeric characters
    let sanitize: String = s.chars().filter(|c| c.is_ascii_alphanumeric()).collect::<String>().to_lowercase();

    // Check if sanitized line reads the same forwards and backwards 
    // it is not a if else statement
    sanitize == sanitize.chars().rev().collect::<String>()
}

fn main() {
    // Taking user input use println for new line
    print!("Type a word or sentence -> ");
    //print as we type
    io::stdout().flush().unwrap();
    let mut word = String::new();
    io::stdin().read_line(&mut word).expect("Failed to read line.");
    let word = word.trim();
    /* Pint nothing or not depening on the output
    if is_palindrome(word) {
        println!("{word} is a palindrome")
    } else {
        println!("{word} is not a palindrome")
    }*/
    println!("\"{word}\" is{} a palindrome.", if is_palindrome(word) { "" } else { " not" });
}
