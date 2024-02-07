import tensorflow as tf
from game import Game
from piece_selector import Selector


NUM_PIECES = 3


g = Game()

selector = Selector(d_model=5, num_heads=8, dff=32, output_size=1)

optimizer = tf.keras.optimizers.Adam(weight_decay=1e-4)

selector.compile(loss=tf.keras.losses.MeanSquaredError(), optimizer=optimizer)

root_state = g.get_board_state()
pieces = g.get_pieces()

test_data = tf.constant([pieces], dtype='float32')
piece_scores = dict(sorted({k:v for v, k in enumerate([float(i[0]) for i in selector(test_data)[0]])}.items(), reverse=True))
best_pieces = []

for idx in piece_scores.values():
    piece = pieces[idx]
    if len(g.board_array[piece[1]][piece[2]][piece[3]][piece[4]].getMovements(g.board_array, f"U{piece[1]}T{piece[2]}{g.rank[piece[4]]}{piece[3] + 1}U0T0a1")) > 0:
        best_pieces.append(pieces[idx])
        if len(best_pieces) == NUM_PIECES:
            break

print(best_pieces)
