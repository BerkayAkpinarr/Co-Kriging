##co kriging

##TEMPERATURE

##Co-krigging for temperature

library(plyr)
library(dplyr)
library(gstat)
library(raster)
library(ggplot2)
library(car)
library(classInt)
library(RStoolbox)
library(spatstat)
library(dismo)
library(fields)
library(gridExtra)
library(Hmisc)
library(automap)



#set your directory to read your csv
setwd("E:/Downscaling/berkay/berkay")
train = read.csv("cnrm-esm2-1_bias_corrected_Only1979.csv")
#names(train)[1] <- "id"

#train = train[-c(2,3)]
train

setwd("E:/Downscaling/berkay/berkay/CorrectedDataRasterShape/ClippedEra5")
new_data = read.csv("era5_elevation_clipped_temperature_csv.csv")
new_data = new_data[-c(3)] # drop unnecessary columns
new_data

names(new_data)[3] <- "elevation"
##make sure the cmip6 values are named as 'cmip6_values' and elevation as 'elevation' and distance as 'Distance'

# create a data frame for the data which will be trained
co.var = train[,c(2,10)] ## cmip6_values and elevation
co.var

cor.matrix = rcorr(as.matrix(co.var))
cor.matrix ## see the correlation and p value 



#plot by omitting the zero elevation values to see correlation
co.var[co.var == 0] <- NA # drop zeros
ggplot(co.var, aes(x=cmip6_values, y=elevation)) + 
  geom_point(shape=1, color="blue")+
  geom_smooth(method=lm, se= FALSE , linetype="dashed",
              color="darkred", fill="blue") +
  labs(x = "CMIP6 Temperature (Kelvin)", y = " Elevation (m)") +
  ggtitle("Temperature (Kelvin) vs Elevation (m) for CMIP6") + theme(plot.title = element_text(hjust=0.5))


#Convert the data frame to a spatial data frame by using sp package.
coordinates(train) = ~lon+lat
coordinates(new_data)=~lon+lat

# Variogram

##autofit with automap package

fit_vgm = autofitVariogram(cmip6_values~elevation, train)
plot(fit_vgm)
temp_krige <- autoKrige(cmip6_values~ elevation, train , new_data)
temp_krige

###IF AUTOVARIOGRAM IS USED, GO TO RASTERIZE DIRECTLY
#convert raster
#CK.pred<-rasterFromXYZ(as.data.frame(CK)[, c("lon", "lat", "cmip6_values.pred")])
temp_krige.pred <- rasterFromXYZ(as.data.frame(temp_krige$krige_output)[, c("lon", "lat", "var1.pred")])

Rasterized_CoKriged<-ggR(temp_krige.pred, geom_raster = TRUE) +
  scale_fill_gradientn("", colours = c("orange", "yellow", "green",  "sky blue","blue"))+
  theme_bw()+
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        axis.title.y=element_blank(),
        axis.text.y=element_blank(),
        axis.ticks.y=element_blank())+
  ggtitle("CK Predicted TEMP")+
  theme(plot.title = element_text(hjust = 0.5))
Rasterized_CoKriged


#write

writeRaster(temp_krige.pred,'E:/Downscaling/berkay/berkay/Temp/bias-corrected-cokriged-temperature_2045.tif')



##option 2 is fitting variogram manually
############## manual fitting #####################
v.soc<-variogram(cmip6_values~ elevation, data = train,cutoff=15, cloud=F)
m.soc<-vgm(psill=22,"Ste",range=9.7,nugget = 0.07) ## change coefficients manually

# least square fit
m.f.soc<-fit.variogram(v.soc, m.soc)
p1<-plot(v.soc, pl=F, model=m.f.soc, main= "Temp")
p1

# Variogram for co-variables

v.ele<-variogram(elevation~ 1, data = train, cloud=F)
# Intial parameter set by eye esitmation
##autofit
fit_elevation = autofitVariogram(elevation~1, train,cutoff=500)
plot(fit_elevation)


# least square fit

m.ele<-vgm(psill=41847,"Ste",range=2.1,kappa = 10) # manual fitting
m.f.ele<-fit.variogram(v.ele, m.ele)
p2<-plot(v.ele, pl=F, model=m.f.ele, main="Ele")
p2
grid.arrange(p1, p2, ncol = 2)  # Multiplot 

#cross-variogram

g <- gstat(NULL, id = "cmip6_values", form = cmip6_values ~ elevation, data=train)
g <- gstat(g, id = "elevation", form = elevation ~ 1, data=train)

v.cross <- variogram(g)
plot(v.cross, pl=F)

g <- gstat(g, id = "cmip6_values", model = m.f.soc,  fill.all=T)
g

g <- fit.lmc(v.cross, g, fit.lmc = TRUE,  correct.diagonal = 1.0) ## use if the correlation has negative sign
g <- fit.lmc(v.cross,g)
g

plot(variogram(g), model=g$model)

##prediction

CK <- predict(g, new_data)
CK.pred<-rasterFromXYZ(as.data.frame(CK)[, c("lon", "lat", "cmip6_values.pred")])

Rasterized_CoKriged<-ggR(CK.pred, geom_raster = TRUE) +
  scale_fill_gradientn("", colours = c("orange", "yellow", "green",  "sky blue","blue"))+
  theme_bw()+
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        axis.title.y=element_blank(),
        axis.text.y=element_blank(),
        axis.ticks.y=element_blank())+
  ggtitle("CK Predicted TEMP")+
  theme(plot.title = element_text(hjust = 0.5))
Rasterized_CoKriged


#write

writeRaster(CK.pred,'E:/Downscaling/berkay/berkay/Temp/bias-corrected-cokriged-temperature_2045.tif')


