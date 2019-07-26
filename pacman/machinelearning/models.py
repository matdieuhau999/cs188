import nn
import numpy as np
import math
PI = math.pi
class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)
        self.dimensions = dimensions
        #print(self.w.shape)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        #print(x.shape)
        #print(self.w)
        #print("3333")
        #print(nn.DotProduct(x,self.w))
        return nn.DotProduct(x,self.w)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        #print("222")
        #print(x)
        #print(nn.as_scalar(x))
        if nn.as_scalar(nn.DotProduct(x,self.w)) >= 0:
            return 1
        return -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"

        batch_size = 1
        i = 0 
        #a = np.ones((self.dimensions,2))
        #print(nn.as_scalar(nn.DotProduct(a,self.w)))
        
        while True:
            update = False
            for x, y in dataset.iterate_once(batch_size):
                if self.get_prediction(x) != nn.as_scalar(y):
                    #print("1")
                    update = True
                    self.w.update(x,nn.as_scalar(y))
            if not update:
                break

class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        
        self.w0 = nn.Parameter(1,100)
        self.b0 = nn.Parameter(1,100)

        self.b1 = nn.Parameter(1,100)
        self.w2 = nn.Parameter(100,50)
        self.b2 = nn.Parameter(1,50)
        self.w3 = nn.Parameter(50,1)
        self.b3 = nn.Parameter(1,1)
        

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        l1 = nn.AddBias(nn.Linear(x,self.w0),self.b0)
        r2 = nn.ReLU(nn.AddBias(l1,self.b1))
        l3 = nn.AddBias(nn.Linear(r2,self.w2),self.b2)
        l4 = nn.AddBias(nn.Linear(l3,self.w3),self.b3)
        return l4

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        #print(nn.SquareLoss(x,y))
        return nn.SquareLoss(self.run(x),y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        batch_size = 1
        
        while True:
            update = False
            for x, y in dataset.iterate_once(batch_size):
                loss= self.get_loss(x,y)
                grad = nn.gradients(loss,[self.w0,self.b0,self.b1,self.w2,self.b2])
                self.w0.update(grad[0], -0.005)
                self.b0.update(grad[1], -0.005)
                self.b1.update(grad[2], -0.005)
                self.w2.update(grad[3], -0.005)
                self.b2.update(grad[4], -0.005)
            if nn.as_scalar(self.get_loss(nn.Constant(dataset.x), nn.Constant(dataset.y))) < 0.02:
                return 

class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.batchsize = 1
        self.w0 = nn.Parameter(784,128)
        self.b0 = nn.Parameter(1,128)
        self.b1 = nn.Parameter(1,128)
        self.w2 = nn.Parameter(128,10)
        self.b2 = nn.Parameter(1,10)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        l1 = nn.AddBias(nn.Linear(x,self.w0),self.b0)
        r2 = nn.ReLU(nn.AddBias(l1,self.b1))
        l2 = nn.AddBias(nn.Linear(r2,self.w2),self.b2)
        return l2

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(x),y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        print(dataset.get_validation_accuracy())
        while True:
            update = False
            for x, y in dataset.iterate_once(self.batchsize):
                loss= self.get_loss(x,y)
                grad = nn.gradients(loss,[self.w0,self.b0,self.b1,self.w2,self.b2])
                self.w0.update(grad[0], -0.005)
                self.b0.update(grad[1], -0.005)
                self.b1.update(grad[2], -0.005)
                self.w2.update(grad[3], -0.005)
                self.b2.update(grad[4], -0.005)
            print(dataset.get_validation_accuracy())
            if dataset.get_validation_accuracy() >= 0.97:
                return 


class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]
        
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.dim = 5 
        self.hidden_dim = 100
        self.batch_size = 2	
        self.w = nn.Parameter(self.num_chars,self.hidden_dim)
        self.w_h = nn.Parameter(self.hidden_dim,self.hidden_dim)
        self.w_f = nn.Parameter(self.hidden_dim,self.dim)
        self.b = nn.Parameter(1,self.dim)

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        h = nn.Linear(xs[0],self.w)
        z = h
        for i, x in enumerate(xs[1:]):
            #print(x)
            z = nn.Add(nn.Linear(x, self.w), nn.Linear(z, self.w_h))
        return nn.AddBias(nn.Linear(z,self.w_f),self.b)

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(xs),y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        i = 0
        a = 0.005
        while True:
            if i >= 10  : a = 0.0025
            if i >= 20 : a = 0.001
            for x, y in dataset.iterate_once(self.batch_size):
                loss = self.get_loss(x,y)
                grad = nn.gradients(loss,[self.w,self.w_h,self.w_f,self.b])
                self.w.update(grad[0], -a)
                self.w_h.update(grad[1], -a)
                self.w_f.update(grad[2], -a)
                self.b.update(grad[3], -a)
            print("dataset.get_validation_accuracy() ",dataset.get_validation_accuracy() )
            i += 1
            if dataset.get_validation_accuracy() >= 0.84:
                return 
