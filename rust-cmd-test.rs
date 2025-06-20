use std::process::Command;
use std::env;

fn main() {
    // [command, arg1, arg2, ...]
    let args: Vec<String> = env::args().collect();
    Command::new(&args[1])
        .args(&args[2..])
        .status()
        .expect("Failed to execute command");
}
