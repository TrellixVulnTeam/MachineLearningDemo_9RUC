import tensorflow as tf

a = tf.Variable(3.0, name='a')

g1 = tf.Graph()
g2 = tf.Graph()

with g1.as_default():
    v = tf.get_variable('v',shape=(1,1),initializer=tf.zeros_initializer())

with g2.as_default():
    v = tf.get_variable('v',shape=(1,1), initializer=tf.ones_initializer())


with tf.Session(graph=g1) as sess:
    tf.initialize_all_variables().run()
    with tf.variable_scope('', reuse=True):
        print(sess.run(tf.get_variable('v')))

with tf.Session(graph=g2) as sess:
    tf.initialize_all_variables().run()
    with tf.variable_scope('', reuse=True):
        print(sess.run(tf.get_variable('v')))

