package com.example.lcs5382.mobilesensordetect;

public class SensorData {
    private int count;
    private double accValueX, accValueY, accValueZ;
    private double oriValueX, oriValueY, oriValueZ;
    private double gyroValueX, gyroValueY, gyroValueZ;
    private double magnoValueX, magnoValueY, magnoValueZ;
    private double pressureValue;





    public int getCount() {
        return count;
    }

    public void setCount(int count) {
        this.count = count;
    }

    public void setAccValueList(double accValueX, double accValueY, double accValueZ){
        setAccValueX(accValueX);
        setAccValueY(accValueY);
        setAccValueZ(accValueZ);
    }

    public void setOriValueList(double oriValueX, double oriValueY, double oriValueZ){
        setOriValueX(oriValueX);
        setOriValueY(oriValueY);
        setOriValueZ(oriValueZ);
    }

    public void setGyroValueList(double gyroValueX, double gyroValueY, double gyroValueZ){
        setGyroValueX(gyroValueX);
        setGyroValueY(gyroValueY);
        setGyroValueZ(gyroValueZ);
    }

    public void setMagnoValueList(double magnoValueX, double magnoValueY, double magnoValueZ){
        setMagnoValueX(magnoValueX);
        setMagnoValueY(magnoValueY);
        setMagnoValueZ(magnoValueZ);
    }

    public String getAccStringList(){
        String data = "";
        data = "" + getAccValueX() + "," + getAccValueY() + "," + getAccValueZ();
        return data;
    }

    public String getOriStringList(){
        String data = "";
        data = "" + getOriValueX() + "," + getOriValueY() + "," + getOriValueZ();
        return data;
    }

    public String getGyroStringList(){
        String data = "";
        data = "" + getGyroValueX() + "," + getGyroValueY() + "," + getGyroValueZ();
        return data;
    }

    public String getMagnoStringList(){
        String data = "";
        data = "" + getMagnoValueX() + "," + getMagnoValueY() + "," + getMagnoValueZ();
        return data;
    }

    public String getPressureStringList(){
        String data = "";
        data = "" + getPressureValue();
        return data;
    }


    public double getAccValueX() {
        return accValueX;
    }

    public void setAccValueX(double accValueX) {
        this.accValueX = accValueX;
    }

    public double getAccValueY() {
        return accValueY;
    }

    public void setAccValueY(double accValueY) {
        this.accValueY = accValueY;
    }

    public double getAccValueZ() {
        return accValueZ;
    }

    public void setAccValueZ(double accValueZ) {
        this.accValueZ = accValueZ;
    }

    public double getOriValueX() {
        return oriValueX;
    }

    public void setOriValueX(double oriValueX) {
        this.oriValueX = oriValueX;
    }

    public double getOriValueY() {
        return oriValueY;
    }

    public void setOriValueY(double oriValueY) {
        this.oriValueY = oriValueY;
    }

    public double getOriValueZ() {
        return oriValueZ;
    }

    public void setOriValueZ(double oriValueZ) {
        this.oriValueZ = oriValueZ;
    }

    public double getGyroValueX() {
        return gyroValueX;
    }

    public void setGyroValueX(double gyroValueX) {
        this.gyroValueX = gyroValueX;
    }

    public double getGyroValueY() {
        return gyroValueY;
    }

    public void setGyroValueY(double gyroValueY) {
        this.gyroValueY = gyroValueY;
    }

    public double getGyroValueZ() {
        return gyroValueZ;
    }

    public void setGyroValueZ(double gyroValueZ) {
        this.gyroValueZ = gyroValueZ;
    }

    public double getMagnoValueX() {
        return magnoValueX;
    }

    public void setMagnoValueX(double magnoValueX) {
        this.magnoValueX = magnoValueX;
    }

    public double getMagnoValueY() {
        return magnoValueY;
    }

    public void setMagnoValueY(double magnoValueY) {
        this.magnoValueY = magnoValueY;
    }

    public double getMagnoValueZ() {
        return magnoValueZ;
    }

    public void setMagnoValueZ(double magnoValueZ) {
        this.magnoValueZ = magnoValueZ;
    }

    public double getPressureValue() {
        return pressureValue;
    }

    public void setPressureValue(double pressureValue) {
        this.pressureValue = pressureValue;
    }
}
