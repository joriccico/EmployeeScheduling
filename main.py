from data import Data
from model import build_model
from solver import solve_model


def main():
    data = Data()
    model, work, obj_bool_vars, obj_bool_coeffs, obj_int_vars, obj_int_coeffs = build_model(data)
    solve_model(model, work, data, obj_bool_vars, obj_bool_coeffs, obj_int_vars, obj_int_coeffs)


if __name__ == "__main__":
    main()
