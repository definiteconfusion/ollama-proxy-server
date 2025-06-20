rustc execute.rs -o execute
if [ $? -ne 0 ]; then
    echo "Compilation failed."
    exit 1
fi
echo "Compilation successful. Executable created: execute"