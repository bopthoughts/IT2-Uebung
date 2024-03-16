from sklearn import metrics
import matplotlib.pyplot as plt

def show_confusion(test, pred):
    cm = metrics.confusion_matrix(test, pred)
    disp = metrics.ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.show()