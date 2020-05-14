// Bubble Sort
func bubble_sort(let lst) {
    let n = len(lst);
    for i := range n {
        for j := range 0...(n-1-i) {
            if lst[j] > lst[j+1] {
                let temp = lst[j];
                lst[j] = lst[j+1];
                lst[j+1] = temp;
            }
        }
    }
    return lst;
}

// Selection Sort
func selection_sort(let lst) {
    let n = len(lst);
    for i := range (n-1) {
        let smallest_idx = i;
        for j := range (i+1)...n {
            if lst[j] < lst[smallest_idx] {
                smallest_idx = j;
            }
        }
        let temp = lst[i];
        lst[i] = lst[smallest_idx];
        lst[smallest_idx] = temp;
    }
    return lst;
}

// Insertion Sort
func insertion_sort(let lst) {
    let n = len(lst);
    for i := range 1...n {
        let j = i;
        let key = lst[j];
        for j > 0 and key < lst[j-1] {
            let temp = lst[j];
            lst[j] = lst[j-1];
            lst[j-1] = temp;
            j -= 1;
            print(lst, j, i);
        }
    }
    return lst;
}

func test(let x) {
    if x == 0 {
        return null;
    }
    print('hi');
}

print(test(0));