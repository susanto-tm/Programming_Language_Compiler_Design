// Variable Declaration
let arr = [1, 3, 2, 5, 1, 0, 2, 3];
let n = 8;

// Bubble Sort Function
func bubble_sort(let lst) {
    for i := range n {
        for j := range 0...(n-1-i) {
            if lst[j] > lst[j+1] {
                let temp = lst[j];
                lst[j] = lst[j+1];
                lst[j+1] = temp;
            }
        }
    }
}

bubble_sort(arr);

print('Sorted array:', arr);