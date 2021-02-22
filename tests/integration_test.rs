use flanders;
use flanders::Vector;

extern crate rand;
use rand::Rng;

use std::fmt::Debug;
use std::fs;
use std::str::FromStr;

fn read_vector<T: FromStr>(file_name: &str) -> Vec<T>
where
    <T as FromStr>::Err: Debug,
{
    let error_message = format!("something went wrong reading file {}", file_name);
    let contents = fs::read_to_string(file_name).expect(&error_message);
    contents.lines().map(|s| s.parse().unwrap()).collect()
}

fn _get_random_vectors(
    num_vectors: usize,
    x_min: f64,
    x_max: f64,
    y_min: f64,
    y_max: f64,
) -> Vec<Vector> {
    let mut rng = rand::thread_rng();
    let mut vectors = Vec::new();

    for _ in 0..num_vectors {
        vectors.push(Vector {
            x: rng.gen_range(x_min, x_max),
            y: rng.gen_range(y_min, y_max),
        });
    }

    vectors
}

#[test]
fn test() {
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

    let tree = flanders::build_tree(&points);

    for (i, observer) in observers.iter().enumerate() {
        let large_number = std::f64::MAX;
        let (index, _) = flanders::nearest_index_from_coordinates(
            0,
            -1,
            large_number,
            &tree,
            &observer,
            &view_vectors[i],
            view_angles_deg[i],
        );
        assert_eq!(index, indices_from_coordinates[i]);
    }
}
