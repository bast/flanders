use flanders;
use flanders::Vector;

extern crate rand;
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

fn get_random_vectors(n: usize) -> Vec<Vector> {
    let mut rng = rand::thread_rng();
    let mut vectors = Vec::new();

    for _ in 0..n {
        vectors.push(Vector {
            x: rng.gen_range(-1.0, 1.0),
            y: rng.gen_range(-1.0, 1.0),
        });
    }

    vectors
}

fn get_random_angles(n: usize) -> Vec<f64> {
    let mut rng = rand::thread_rng();
    let mut angles = Vec::new();

    for _ in 0..n {
        angles.push(rng.gen_range(5.0, 90.0));
    }

    angles
}

#[test]
fn noddy() {
    let points: Vec<Vector> = read_vector("tests/reference/points.txt");
    let view_vectors: Vec<Vector> = read_vector("tests/reference/view_vectors.txt");
    let view_angles_deg: Vec<f64> = read_vector("tests/reference/angles.txt");

    let indices_from_indices: Vec<i32> =
        read_vector("tests/reference/nearest_indices_from_indices.txt");
    for i in 0..points.len() {
        let index = flanders::nearest_index_from_index_noddy(
            &points,
            i,
            &view_vectors[i],
            view_angles_deg[i],
        );
        assert_eq!(index, indices_from_indices[i]);
    }

    let observers: Vec<Vector> = read_vector("tests/reference/observers.txt");
    let indices_from_coordinates: Vec<i32> =
        read_vector("tests/reference/nearest_indices_from_coordinates.txt");
    for (i, observer) in observers.iter().enumerate() {
        let index = flanders::nearest_index_from_coordinates_noddy(
            &points,
            &observer,
            &view_vectors[i],
            view_angles_deg[i],
        );
        assert_eq!(index, indices_from_coordinates[i]);
    }
}

#[test]
fn tree() {
    let n = 5_000;

    let points = get_random_vectors(n);
    let observers = get_random_vectors(n);
    let view_vectors = get_random_vectors(n);
    let view_angles_deg = get_random_angles(n);

    let start = Instant::now();
    let mut indices_noddy = Vec::new();
    for (i, observer) in observers.iter().enumerate() {
        let index = flanders::nearest_index_from_coordinates_noddy(
            &points,
            &observer,
            &view_vectors[i],
            view_angles_deg[i],
        );
        indices_noddy.push(index);
    }
    println!("time elapsed in noddy: {:?}", start.elapsed());

    let start = Instant::now();
    let tree = flanders::build_tree(&points);
    println!("time elapsed in building tree: {:?}", start.elapsed());

    let start = Instant::now();
    let indices = flanders::nearest_indices_from_coordinates(
        &tree,
        &observers,
        &view_vectors,
        &view_angles_deg,
    );
    println!(
        "time elapsed in nearest_indices_from_coordinates: {:?}",
        start.elapsed()
    );

    assert_eq!(indices, indices_noddy);
}
