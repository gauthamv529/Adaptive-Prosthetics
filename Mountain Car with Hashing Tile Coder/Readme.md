
#Explanation for Rich Sutton's Tile Coder#
  * tiles                   ; a provided array for the tile indices to go into
  * starting-element        ; first element of "tiles" to be changed (typically 0)
  * num-tilings             ; the number of tilings desired
  * memory-size             ; the number of possible tile indices
  * floats                  ; a list of real values making up the input vector
  * ints                    ; list of optional inputs to get different hashings
  

The float variables will be gridded at unit intervals, so generalization will be by approximately 1 in each direction, and any scaling will have 
to be done externally before calling tiles.

It is recommended by the UNH folks that numtilings be a power of 2, e.g., 16. 

My understanding of the above is that the input space is infinite (Real number space) and the grids are at unit intervals (for e.g., a 1D space would have intervals at 1,2,3,.. ).
Scaling the inputs should be done accordingly. 
Note: Inputs should be scaled before feeding it as input to the tilecoder.
