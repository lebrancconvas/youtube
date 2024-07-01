use std::io;
use rand::Rng;
use std::cmp::Ordering;

fn main() {
    println!("Guess a number nerd");
    let mut guess = String::new();                                      
    io::stdin().read_line(&mut guess).expect("Failed to get input."); 
    let guess: u32 = guess.trim().parse().expect("Please provide a number");
    println!("You guessed {}", guess);
    
    let secret_number = rand::thread_rng().gen_range(1..=100);

    match guess.cmp(&secret_number) {
        Ordering::Less => println!("Lesser value value"),
        Ordering::Greater => println!("Greater value"),
        Ordering::Equal => println!("Match found"),
    }

   println!("The secrent number is {}", secret_number);

                                                                        

 
 
 
}
