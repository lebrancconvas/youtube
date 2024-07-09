use std::io;

fn is_palindrome(s: &String) -> bool {
    // Convert the input string to lowercase and filter out non-alphanumeric characters
    let sanitize: String = s
        .chars()
        .filter(|c| c.is_ascii_alphanumeric())
        .collect::<String>()
        .to_lowercase();

    // Check if clean_str reads the same forwards and backwards
    sanitize == sanitize.chars().rev().collect::<String>()
}

fn main() {
    // Test cases
    println!("Type a word or sentence ->");
    let mut word = String::new();
    io::stdin().read_line(&mut word).expect("Failed to read line.");
    // Check each test case and print the result
    println!("\"{word}\" is{} a palindrome.", if is_palindrome(&mut word) { "" } else { " not" });
}
