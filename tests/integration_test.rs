use flanders;

use rand::Rng;

use std::fmt::Debug;
use std::fs;
use std::str::FromStr;

use std::time::Instant;

fn read_vector<T: FromStr>(file_name: &str) -> Vec<T>
where
    <T as FromStr>::Err: Debug,
{
    let error_message = format!("something went wrong reading file {}", file_name);
    let contents = fs::read_to_string(file_name).expect(&error_message);
    contents.lines().map(|s| s.parse().unwrap()).collect()
}

fn read_tuples(file_name: &str) -> Vec<(f64, f64)> {
    let error_message = format!("something went wrong reading file {}", file_name);
    let contents = fs::read_to_string(file_name).expect(&error_message);

    let mut tuples = Vec::new();

    for line in contents.split("\n") {
        let words: Vec<&str> = line.split_whitespace().collect();
        if words.len() == 2 {
            let x = words[0].parse().unwrap();
            let y = words[1].parse().unwrap();
            tuples.push((x, y));
        }
    }

    tuples
}

fn get_random_vectors(n: usize) -> Vec<(f64, f64)> {
    let mut rng = rand::rng();
    let mut vectors = Vec::new();

    for _ in 0..n {
        vectors.push((rng.random_range(-1.0..1.0), rng.random_range(-1.0..1.0)));
    }

    vectors
}

fn get_random_angles(n: usize) -> Vec<f64> {
    let mut rng = rand::rng();
    let mut angles = Vec::new();

    for _ in 0..n {
        angles.push(rng.random_range(5.0..90.0));
    }

    angles
}

#[test]
fn noddy() {
    let points: Vec<(f64, f64)> = read_tuples("tests/reference/points.txt");
    let view_vectors: Vec<(f64, f64)> = read_tuples("tests/reference/view_vectors.txt");
    let view_angles_deg: Vec<f64> = read_vector("tests/reference/angles.txt");

    let indices_reference: Vec<i32> =
        read_vector("tests/reference/nearest_indices_from_indices.txt");
    let observer_indices: Vec<_> = (0..points.len()).collect();
    let indices_noddy = flanders::nearest_indices_from_indices_noddy(
        &points,
        &observer_indices,
        &view_vectors,
        &view_angles_deg,
    );
    assert_eq!(indices_reference, indices_noddy);

    let observer_coordinates: Vec<(f64, f64)> = read_tuples("tests/reference/observers.txt");
    let indices_reference: Vec<i32> =
        read_vector("tests/reference/nearest_indices_from_coordinates.txt");
    let indices_noddy = flanders::nearest_indices_from_coordinates_noddy(
        &points,
        &observer_coordinates,
        &view_vectors,
        &view_angles_deg,
    );
    assert_eq!(indices_reference, indices_noddy);
}

#[test]
fn tree_indices_from_coordinates() {
    let n = 5_000;

    let points = get_random_vectors(n);
    let observer_coordinates = get_random_vectors(n);
    let view_vectors = get_random_vectors(n);
    let view_angles_deg = get_random_angles(n);

    let start = Instant::now();
    let indices_noddy = flanders::nearest_indices_from_coordinates_noddy(
        &points,
        &observer_coordinates,
        &view_vectors,
        &view_angles_deg,
    );
    println!("time elapsed in noddy: {:?}", start.elapsed());

    let start = Instant::now();
    let tree = flanders::build_search_tree(points);
    println!("time elapsed in building tree: {:?}", start.elapsed());

    let start = Instant::now();
    let indices = flanders::nearest_indices_from_coordinates(
        tree,
        observer_coordinates,
        view_vectors,
        view_angles_deg,
    );
    println!(
        "time elapsed in nearest_indices_from_coordinates: {:?}",
        start.elapsed()
    );

    assert_eq!(indices, indices_noddy);
}

#[test]
fn tree_indices_from_indices() {
    let n = 5_000;

    let points = get_random_vectors(n);
    let observer_indices: Vec<_> = (0..points.len()).collect();
    let view_vectors = get_random_vectors(n);
    let view_angles_deg = get_random_angles(n);

    let start = Instant::now();
    let indices_noddy = flanders::nearest_indices_from_indices_noddy(
        &points,
        &observer_indices,
        &view_vectors,
        &view_angles_deg,
    );
    println!("time elapsed in noddy: {:?}", start.elapsed());

    let start = Instant::now();
    let tree = flanders::build_search_tree(points);
    println!("time elapsed in building tree: {:?}", start.elapsed());

    let start = Instant::now();
    let indices = flanders::nearest_indices_from_indices(
        tree,
        observer_indices,
        view_vectors,
        view_angles_deg,
    );
    println!(
        "time elapsed in nearest_indices_from_indices: {:?}",
        start.elapsed()
    );

    assert_eq!(indices, indices_noddy);
}
