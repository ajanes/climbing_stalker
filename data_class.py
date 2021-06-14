class Data:

    def __init__(self, id, x_position, y_position, z_position, x_velocity, y_velocity, z_velocity, x_dimensions, y_dimensions, z_dimensions):
        self.id = id
        self.position = []
        self.position.append(x_position)
        self.position.append(y_position)
        self.position.append(z_position)
        self.velocity = []
        self.velocity.append(x_velocity)
        self.velocity.append(y_velocity)
        self.velocity.append(z_velocity)
        self.dimensions = []
        self.dimensions.append(x_dimensions)
        self.dimensions.append(y_dimensions)
        self.dimensions.append(z_dimensions)
