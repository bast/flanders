#ifndef DISTANCE_H_INCLUDED
#define DISTANCE_H_INCLUDED

double get_distance(const node *leaf, const double coordinates[2]);

double signed_distance_to_split(const node *leaf, const double coordinates[2]);

int get_position(const node *leaf, const double coordinates[2]);

#endif /* DISTANCE_H_INCLUDED */
