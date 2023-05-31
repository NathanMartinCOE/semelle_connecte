library(epiR)
library(ggplot2)
library(dplyr)
library(irr)
library(flextable)



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
        Return rval.ccc -> a dataframe with the CCL value and the 95% IC of the CCL.
        And plot of the concordance beetween the two method is show.
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
    scale_x_continuous(name = "TDM6") + #method1 = TDM6
    scale_y_continuous(name = "SRU") +  #method2 = SRU
    coord_fixed(ratio = 1 / 1)+
    theme_classic()+
    labs(caption = rval.lab$lab)+
    theme(plot.caption = element_text(hjust = 0.5))+
    ggtitle("Lin Concordance correlation plot")+
    labs(subtitle = parametre) +
    theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5))
  print(CCL_plot)
  
  return(rval.ccc)
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
    scale_y_continuous(limits = c(rval.ba$sblalt$lower -10, rval.ba$sblalt$upper + 10), name = "Difference of dynamic symetry function")+
    theme_classic()+
    ggtitle("Bland and Altman plot")+
    labs(subtitle = parametre) +
    theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5))
  print(BAA_plot)
  
  return(rval.ba)
}

### ================================================ Path of Dataset of each method ================================================
" 
For more information about the Dataset please see the python script :           Etude_Assym_Compute_R_dataset.py 
                                                       Available at :           https://github.com/NathanMartinCOE/semelle_connecte 
"
# Data Localisation
#DataPath_TDM = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\Etude_TDM_SRU\\DynamicSymetryScoreMean_TDM.csv"
#DataPath_SRU = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\Etude_TDM_SRU\\DynamicSymetryScoreMean_SRU.csv"
DataPath_TDM = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\Etude_TDM_SRU\\FALSE_DynamicSymetryScoreMean_TDM.csv"
DataPath_SRU = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\Etude_TDM_SRU\\FALSE_DynamicSymetryScoreMean_SRU.csv"

data_TDM = read.csv(DataPath_TDM)
data_TDM = data_TDM[2:6] # Because of pandas indexing in python i took of the first col which is index
data_SRU = read.csv(DataPath_SRU) 
data_SRU = data_SRU[2:6] # Because of pandas indexing in python i took of the first col which is index


### ====================== Instantiates vectors with a "delete" value to check that it hasn't been taken ============================

# Vectors for tab Results
names_parametre     <- "delete"
values_mean_method1 <- "delete"
values_std_method1  <- "delete"
values_mean_method2 <- "delete"
values_std_method2  <- "delete"
values_ccl_est      <- "delete"
values_ccl_low      <- "delete"
values_ccl_up       <- "delete"
values_ccl_prec     <- "delete"
values_ccl_accu     <- "delete"

# vector for tab BA_Description
values_BA_est       <- "delete"
values_BA_lower     <- "delete"
values_BA_upper     <- "delete"


### ====================== Iteration for compute and plot CCL and B&A between the tow method for each parametre  ====================

for (parametre in names(data_TDM)){
  method1 = data_TDM[[parametre]]
  method2 = data_SRU[[parametre]]
  dataset <- data.frame(method1, method2)
  rval.ccc <- ConcordanceCorrelationCoefficient(dataset=dataset, parametre=parametre)
  rval.ba <- BlandAltman(dataset=dataset, parametre=parametre)
  ### ==================== Complete the vectors to generate the results table =============
  names_parametre     <- c(names_parametre, parametre)
  values_mean_method1 <- c(values_mean_method1, round(mean(data_TDM[[parametre]]), digits = 2))
  values_std_method1  <- c(values_std_method1, round(sd(data_TDM[[parametre]]), digits = 2))
  values_mean_method2 <- c(values_mean_method2, round(mean(data_SRU[[parametre]]), digits = 2))
  values_std_method2  <- c(values_std_method2, round(sd(data_SRU[[parametre]]), digits = 2))
  values_ccl_est      <- c(values_ccl_est, round(rval.ccc$rho.c[,1], digits = 2))
  values_ccl_low      <- c(values_ccl_low, round(rval.ccc$rho.c[,2], digits = 2))
  values_ccl_up       <- c(values_ccl_up, round(rval.ccc$rho.c[,3], digits = 2))
  values_ccl_prec     <- c(values_ccl_prec, round(epi.occc(dataset)$oprec, digits = 2))
  values_ccl_accu     <- c(values_ccl_accu, round(epi.occc(dataset)$oaccu, digits = 2))
  ### ==================== Complete the vectors to generate the Bland & Altman table ========
  values_BA_est       <- c(values_BA_est, round(rval.ba$sblalt$est, digits = 2))
  values_BA_lower     <- c(values_BA_lower, round(rval.ba$sblalt$lower, digits = 2))
  values_BA_upper     <- c(values_BA_upper, round(rval.ba$sblalt$upper, digits = 2))
}

### ============================================== Creation of the results table  =====================================================
# I change the names_parametre for aesthetics
names_parametre <- c("Stance Duration", "Single Support Duration", "Double Support Duration", "Swing Duration", "Vertical Ground Reaction Force")

Results <- data.frame(
                      "Paramètres" = names_parametre,
                      "TDM6"       = paste(values_mean_method1[2:6], "±", values_std_method1[2:6], sep = " "), 
                      "SRU"        = paste(values_mean_method2[2:6], "±", values_std_method2[2:6], sep = " "),
                      "CCL"        = values_ccl_est[2:6],
                      "IC_95"      = paste(values_ccl_low[2:6], "-", values_ccl_up[2:6], sep = " "), 
                      "Précision"  = values_ccl_prec[2:6],
                      "Exactitude" = values_ccl_accu[2:6]
                      )

# I use flextable for aesthetics table
ft <- flextable(Results)
ft <- theme_vanilla(ft)
ft <- bg(ft,i = c(1,3,5), bg = "lightgrey")
ft <- width(ft, j = 1:7, width = dim_pretty(ft)$widths)
ft <- align(ft, align = "center", part = "header")
ft <- align(ft, i = 1:5, j = 2:7, align = "center")
ft

### =========================================== Creation of the Bland & Altman descripton table  =========================================


BA_Description <- data.frame(
                            "Paramètres"  = names_parametre,
                            "Biais"       = values_BA_est[2:6],
                            "Lower"       = values_BA_lower[2:6], # Limits of Agreements
                            "Upper"       = values_BA_upper[2:6]  # Limits of Agreements
)

ft_BA <- flextable(BA_Description)
ft_BA <- width(ft_BA, j = 1:4, width = dim_pretty(ft_BA)$widths)
ft_BA

### ===================================================== Save tables in a word ===========================================================


save_as_docx(ft, ft_BA , path="C:\\Users\\Nathan\\Desktop\\Recherche\\R_studio\\Etude_Assym\\FALSE\\Results_table.docx")
#save_as_docx(ft, ft_BA , path="C:\\Users\\Nathan\\Desktop\\Recherche\\R_studio\\Etude_Assym\\Results_table.docx")


