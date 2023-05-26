library(epiR)
library(ggplot2)
library(dplyr)
library(irr)

### ================================================ Definition of functions ======================================================

ConcordanceCorrelationCoefficient <- function(dataset, parametre){
  "
  ================================================== Documentation ===============================================
  This function compute and plot Lin's concordance coefficient.
      Lin LIK. A Concordance Correlation Coefficient to Evaluate Reproducibility. Biometrics. mars 1989;45(1):255.
  
  Args :
        dataset --> (dataframe) The dataframe contains the data from methods 1 and 2 in each column.
                      /!\ The column names must be method1 and method2.
        parametre --> (str) The name of the parameter measured by the methods.
        
  Outputs:
        This function dont return anything but a plot of the concordance beetween the two method is show.
  "
  
  method1 = dataset$method1
  method2 = dataset$method2
  ### Concordance correlation coefficient
  rval.ccc <- epi.ccc(method1, method2, ci = "z-transform", conf.level = 0.95, rep.measure = FALSE)
  rval.lab <- data.frame(lab = paste("CCC: ", 
                                     round(rval.ccc$rho.c[,1], digits = 2), " (95% CI ", 
                                     round(rval.ccc$rho.c[,2], digits = 2), " - ", 
                                     round(rval.ccc$rho.c[,3], digits = 2), ")", sep = "")) 
  z <- lm(method2 ~ method1) 
  alpha <- summary(z)$coefficients[1,1] 
  beta <- summary(z)$coefficients[2,1] 
  rval.lm <- data.frame(alpha, beta)
  
  ### Concordance correlation plot
  CCL_plot <- ggplot(data = dataset, aes(x = method1, y = method2)) +
    geom_point() +
    geom_abline(intercept = 0, slope = 1) +
    geom_abline(data = rval.lm, aes(intercept = alpha, slope = beta), linetype = "dashed") +
    scale_x_continuous(name = "Method 1") +
    scale_y_continuous(name = "Method 2") +
    coord_fixed(ratio = 1 / 1)+
    theme_classic()+
    labs(caption = rval.lab$lab)+
    theme(plot.caption = element_text(hjust = 0.5))+
    ggtitle("Lin Concordance correlation plot")+
    labs(subtitle = parametre) +
    theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5))
  print(CCL_plot)
}

BlandAltman <- function(dataset, parametre){
  "
  ================================================== Documentation ===============================================
  This function plot Bland and Altman's graphics.
      Bland JM, Altman DG. Statistical methods for assessing agreement between two methods of clinical measurement. 
      Lancet. 8 févr 1986;1(8476):307‑10. 

  Args :
        dataset --> (dataframe) The dataframe contains the data from methods 1 and 2 in each column.
                      /!\ The column names must be method1 and method2.
        parametre --> (str) The name of the parameter measured by the methods.
        
  Outputs:
        This function dont return anything but plot Bland and Altman's graphics for the two method.
  "
  method1 = dataset$method1
  method2 = dataset$method2
  ### Bland and Altman plot (from Bland and Altman 1986):
  x <-method1
  y <- method2
  
  rval.ba <- epi.ccc(x, y, ci = "z-transform", conf.level = 0.95, rep.measure = FALSE)
  method_mean = rval.ba$blalt[,1]
  method_delta = rval.ba$blalt[,2]
  
  BAA_plot <- ggplot(data = rval.ba$blalt, aes(x = mean, y = delta)) + 
    geom_point() + 
    geom_hline(data = rval.ba$sblalt, aes(yintercept = lower), linetype = 2) + 
    geom_hline(data = rval.ba$sblalt, aes(yintercept = upper), linetype = 2) + 
    geom_hline(data = rval.ba$sblalt, aes(yintercept = est), linetype = 1) + 
    scale_x_continuous(limits = c(min(method_mean),max(method_mean)), name = "Average of dynamic symetry function") + 
    scale_y_continuous(limits = c(-10,10), name = "Difference of dynamic symetry function")+
    theme_classic()+
    ggtitle("Bland and Altman plot")+
    labs(subtitle = parametre) +
    theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5))
  print(BAA_plot)
}

### ================================================ Path of Dataset of each method ================================================
" 
For more information about the Dataset please see the python script :           Etude_Assym_Compute_R_dataset.py 
                                                       Available at :           https://github.com/NathanMartinCOE/semelle_connecte 
"

DataPath_TDM = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\Etude_TDM_SRU\\DynamicSymetryScoreMean_TDM.csv"
DataPath_SRU = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\Etude_TDM_SRU\\DynamicSymetryScoreMean_SRU.csv"
data_TDM = read.csv(DataPath_TDM)
data_TDM = data_TDM[2:6] # Because of pandas indexing in python i took of the first col which is index
data_SRU = read.csv(DataPath_SRU) 
data_SRU = data_SRU[2:6] # Because of pandas indexing in python i took of the first col which is index

### ====================== Iteration for compute and plot CCL and B&A between the tow method for each parametre  ====================

for (parametre in names(data_TDM)){
  method1 = data_TDM[[parametre]]
  method2 = data_SRU[[parametre]]
  dataset <- data.frame(method1, method2)
  ConcordanceCorrelationCoefficient(dataset=dataset, parametre=parametre)
  BlandAltman(dataset=dataset, parametre=parametre)
}
  
