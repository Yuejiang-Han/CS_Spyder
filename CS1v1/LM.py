import numpy as np

class LinearRegression:
    def __init__(self):
        self.coefficients = None

    def fit(self, X, y):
        # 添加偏置项
        X = np.c_[np.ones(X.shape[0]), X]
        # 计算系数
        self.coefficients = np.linalg.inv(X.T @ X) @ X.T @ y

    def predict(self, X):
        # 添加偏置项
        X = np.c_[np.ones(X.shape[0]), X]
        return X @ self.coefficients


# 创建一个 LinearRegression 类的实例
model = LinearRegression()

# 准备训练数据
X_train = np.array([[8], [9], [18], [26], [35]])
y_train = np.array([2, 4, 6, 8, 10])

# 训练模型
model.fit(X_train, y_train)

# 使用模型进行预测
X_new = np.array([[98]]) 
y_pred = model.predict(X_new) 
print("预测结果：", y_pred) 
