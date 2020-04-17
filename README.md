# Arithmitic Coding 



### Diffrent block sizes effect
|4|8|16|
|--|--|--|
|![4](https://user-images.githubusercontent.com/44725090/79596638-31386d80-80e1-11ea-842b-2824e9c4d72a.jpg)|![8](https://user-images.githubusercontent.com/44725090/79595847-dc482780-80df-11ea-8117-1429790389bf.png)|![16](https://user-images.githubusercontent.com/44725090/79595985-15809780-80e0-11ea-8688-3df7db3a0308.png)|
***
## Encoding
- Input
	- an image `(jpg , png , ..etc)`
	- output_file  `string`    `name of the output file`
	- block_size  `int`   
	- float_size  `int` `(16 , 32 , 64) only`  
- Generated Files
	- prob `npy`  `it is generated without specifying its name`
	- 'output_file'  `.npy` `encoded compressed file`
## Decoding
- Input `expects prob.npy to be in the same directory of the encoded file`
	- input_file `.npy` `the encoded file`
	- output_file  `string`    `name of the output file`
	- width 	`width of the original photo`
	 - height `height of the original photo`
	- block_size  `int`   
- Generated Files
	- 'output_file'  `jpg` `decoded image`
	
## How to run
start the file using the terminal with the input as system arguments as the following
- Encode
	```python arith.py encode <input_file> <output_file> <block_size><float_size>```
	Example 
	```python arith.py encode "test.jpg" encoded_test 16 64```
	Output
	- prob.npy
	- encoded_test.npy

- Decode
block_size must be the same as the one used in encoding
prob.npy must be in the same directory as the encoded npy file
	```python arith.py decode <input_file> <output_file> <width> <height> <block_size>```
	Example 
	```python arithmetic.py decode 'encoded_test.npy' 'decoded_test.jpg' 1280 720 16```
	Output
	- decoded_test.jpg
