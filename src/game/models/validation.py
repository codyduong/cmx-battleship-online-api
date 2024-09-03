from django_utils_morriswa.exceptions import ValidationException, BadRequestException



VALID_COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
VALID_ROWS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']


def ensure_valid_tile_id(tile: str) -> (str, str):
    col = tile[0]
    row = tile[1::]
    if col not in VALID_COLUMNS:
        raise BadRequestException('invalid column identifier')

    if row not in VALID_ROWS:
        raise BadRequestException('invalid row identifier')

    return (col, row)


def ensure_valid_ship_row(ship_len: int, ship_collection: list[str]):
    last_col: str = None
    last_row: str = None
    for tile in ship_collection:
        if last_col is None and last_row is None:
            (last_col, last_row) = ensure_valid_tile_id(tile)
        else:
            (col, row) = ensure_valid_tile_id(tile)

            if col != last_col and row != last_row:
                raise ValidationException(f'ship_{ship_len}', 'ships must share similar row or column ie no diagonals')
            elif (col != last_col and row == last_row
                  and col != VALID_COLUMNS[VALID_COLUMNS.index(last_col) - 1]
                  and col != VALID_COLUMNS[VALID_COLUMNS.index(last_col) + 1]):
                    raise ValidationException(f'ship_{ship_len}',
                                              'ships must share at least 1 border')
            elif (col == last_col and row != last_row
                  and row != VALID_ROWS[VALID_ROWS.index(last_row) - 1]
                  and row != VALID_ROWS[VALID_ROWS.index(last_row) + 1]):
                    raise ValidationException(f'ship_{ship_len}',
                                              'ships must share at least 1 border')

            last_col = col
            last_row = row
