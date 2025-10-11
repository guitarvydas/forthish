1. Modify `xword` to parse Forthish comments and to ignore them. A Forthish comment is any text enclosed in parentheses `( ... )`. 
2. Consider: is `xword` the right place to recognize and ignore comments?
3. Add a word to multiply the top two stack integers together, called `*`. The top two stack items are consumed and the result of the multiplication is pushed onto the stack. Use Python multiplication. 
4. Add a word to divide the top two stack integers together, called `/`. The top integer is divided by the second integer. The truncated result is pushed onto the stack.
5. Consider: what if the stack only contains integers that are only 16-bits each? I.E. an integer is only in the range of 0..65535. What happens when `A B +` or `A B *` is too large to fit into 16 bits, i.e. a number greater than 65,536?
6. Consider: what if the stack only contains integers that are only 16-bits each? What happens when `A B -` is negative?
7. Consider: what happens when `A B /` has a remainder? I.E. the answer isn't just a single integer, but an integer plus some left-over.