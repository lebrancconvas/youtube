// here we'll have all the files, libraries, modules etc.

//import libraries 
//
use std::io::{self, Write};

// let's define the function which will check for the palindrome
//s will refer to a str which will return a boolean value 
fn palindrome(s: &str) -> bool {
    // sanitize the variable s with alphanumerics
    // chars iterates over all the characters and filter removes all the commas and periods,
    // collect then joins all the characters and returns a string 
    let sanitize: String = s.
        chars().
        filter(|c| c.is_ascii_alphanumeric())
        .collect::<String>()
        .to_lowercase();
    // compare to the reverse value of every char and collect it into a string.

    sanitize == sanitize
        .chars()
        .rev()
        .collect::<String>()
}

//create function like this

fn main() {
    //but the prompt is on a new line , let's fix that
    print!("Type a word -> ");
    io::stdout().flush().unwrap();
    // take user input with the io library 
    // mut means mutable. generally a variable is immutable.
    // define a variable which will store this input
    let mut word = String::new();
    io::stdin().read_line(&mut word).expect("Failed to read.");
    let word = word.trim(); //trim the whitespace after taking the input
    //print the variable
    // the new line there because of rust's feature
    // we'll see how to remove that in future.
    if palindrome(word) {
        println!("{word} -> is A palindrome.");
    } else {
        println!("{word} -> is not a palindrome.");
    }

}













