func hashtag(let i, let j) {
    if i <= 0 or i > j {
        return 0;
    }

    print(i * "#");

    hashtag(i - 1, j);
}

hashtag(3, 4);