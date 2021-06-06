import java.util.List;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.function.BiFunction;
import java.util.stream.Stream;
import java.util.Scanner;
import java.util.Timer;
import java.util.TimerTask;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;


import io.reactivex.Observable;
import io.reactivex.Single;
import io.reactivex.Flowable;
import io.reactivex.schedulers.Schedulers;
import java.net.URLConnection;
import java.net.URL;
import java.sql.DriverManager;
import java.sql.Statement;
import java.sql.Connection;
import java.sql.ResultSet;
import org.davidmoten.rx.jdbc.Database;
import org.davidmoten.rx.pool.Pool;
import org.davidmoten.rx.jdbc.pool.Pools;

import io.vavr.control.Try;

class DemoThread extends Thread {
  public void run()
  {
    System.out.println("Thread " + Thread.currentThread() + " is running");
  }
}

class Helper extends TimerTask
{
  public void run()
  {
    System.out.println("Timeout");
    System.exit(0);
  }
}

class MultiplyThread extends Thread {
  private final ArrayList<ArrayList<Integer>> a;
  private final ArrayList<ArrayList<Integer>> b;
  private int row;
  private final ArrayList<Integer> result;
	
  public MultiplyThread(int row, ArrayList<ArrayList<Integer>> a, ArrayList<ArrayList<Integer>> b)
  {
    this.a = a;
    this.b = b;
    this.row = row;
    this.result = new ArrayList<Integer>();
  }
	
  public void run()
  {
    for(int i = 0; i < b.size(); i++)
    {
      
      int resultVal = 0;
      int aLength = a.get(row).size();
      for(int j = 0; j < aLength; j++)
      {
        resultVal += a.get(row).get(j) * b.get(j).get(i); 
      }
	    
	
      result.add(resultVal);
    }
  }

  public ArrayList<Integer> getResult()
  {
    return this.result;
  }
	
}




class PiThread extends Thread {
  private final int threadCount;
  private final int n;
  private final int threadReminder;
  private double sum;
	

  public PiThread(int threadCount, int threadReminder, int n)
  {
    this.threadCount = threadCount;
    this.threadReminder = threadReminder;
    this.n = n;
    sum = 0;
  }
  public void run() 
  {

    for(int i = 0; i < n; i++) 
    {
      if(i % threadCount == threadReminder)
      {
        sum += Math.pow(-1, i) / (2 * i + 1);
      }    
    }
  }
        
  public double getSum() 
  {
    return sum;
  }
}

class Main
{


public static void printArrayList(List<ArrayList<Integer>> array)
{
    for(int i = 0; i < array.size(); i++)
    {
      for(int j = 0; j < array.get(i).size(); j++)
      {
        if(j == (array.get(i).size() - 1))
        { 
 	  System.out.println(array.get(i).get(j));
        }
	else{
	  System.out.print(array.get(i).get(j) + "|");
	}
      } 
    }
}

  public static void printArray(int[][] array)
{
    int cols = array.length;
    int rows = array[0].length;


    for(int i = 0; i < cols; i++)
    {
      for(int j = 0; j < rows; j++)
      {
        if(j == (rows - 1))
        { 
 	  System.out.println(array[i][j]);
        }
	else{
	  System.out.print(array[i][j] + "|");
	}
      } 
    }

}

  public static int[][] generateInput(int cols, int rows){
    
    int[][] input = new int[cols][rows];
    for(int i = 0; i < cols; i++)
    {
      for(int j = 0; j < rows; j++)
      {
        input[i][j] = j;
      } 
    }
    return input;
  }

  public static int[][] generateKernel(int cols, int rows){
    int[][] kernel = new int[cols][rows];
    for(int i = 0; i < cols; i++)
    {
      for(int j = 0; j < rows; j++)
      {
        kernel[i][j] = i;
      } 
    }
    return kernel;
  }

  public static ArrayList<Integer> multiplyRow(int row, ArrayList<ArrayList<Integer>> a, ArrayList<ArrayList<Integer>> b)
  {

    ArrayList<Integer> result = new ArrayList<Integer>();
    int length = b.get(0).size();

 
    //loop through all columns of b

    for(int i = 0; i < length; i++)
    {
      
      int resultVal = 0;
      int aLength = a.get(row).size();
      for(int j = 0; j < aLength; j++)
      {

	resultVal += a.get(row).get(j) * b.get(j).get(i); 
      	
      }
	
      result.add(resultVal);
    }
    System.out.println(Thread.currentThread());
    return result;

  }



  public static int[][] convolute(int[][] in, int[][]kernel, int kCols, int kRows, int rows, int cols)
  {

			
    int kCenterX = kCols / 2;
    int kCenterY = kRows / 2;

    int out[][] = new int[rows][cols];
			
    
			
			
    for(int i=0; i < rows; ++i)              // rows
    {
      for(int j=0; j < cols; ++j)          // columns
      {
	for(int m=0; m < kRows; ++m)     // kernel rows
	{
	  int mm = kRows - 1 - m;      // row index of flipped kernel
          for(int n=0; n < kCols; ++n) // kernel columns
	  {
            int nn = kCols - 1 - n;  // column index of flipped kernel

			                // index of input signal, used for checking boundary
            int ii = i + (kCenterY - mm);
	    int jj = j + (kCenterX - nn);

			                // ignore input samples which are out of bound
            if( ii >= 0 && ii < rows && jj >= 0 && jj < cols )
	    out[i][j] += in[ii][jj] * kernel[mm][nn];
	  }
	}
      }
    }
			
    for(int i = 0; i < rows; i++)
    {
      for(int j = 0; j < cols; j++)
      {
	if(j == cols - 1)
        {
	  System.out.println(out[i][j]);
	}
	else {
	  System.out.print(out[i][j] + " ");
	}
      }
     }
	
  return out;

  } 

	public static ArrayList<ArrayList<Integer>> getArray()
	{
		
    		int vertexCount = 3;
            ArrayList<ArrayList<Integer>> graph = new ArrayList<>(vertexCount);
        
            for(int i = 0; i < vertexCount; i++)
            {
                graph.add(new ArrayList<Integer>());
            }  
        
            for(int i = 0; i < vertexCount; i++)
            {
                for(int a = 0; a < vertexCount; a++)
                {
                    graph.get(i).add((i * vertexCount) + (a + 1));
                }
            }
		    return graph;
		    
		}
    


  private static double calcPi(final int threadCount, final int threadReminder, final int n)
  {
    double sum = 0.0;

    for(int i = 0; i < n; i++)
    {
      if(i % threadCount == threadReminder)
      {
        sum += Math.pow(-1, i) / (2 * i + 1);
      }
    }

    return sum;
  }
  
  private static Connection createDatabase() throws Exception 
  {
    Connection con = null;    
    Class.forName("org.sqlite.JDBC");
    con = DriverManager.getConnection("jdbc:sqlite:C:/sqlite/db/Gutnic.db");
    
    if (con != null) 
    {
    
      Statement stmt = con.createStatement();
      stmt.executeUpdate("CREATE TABLE IF NOT EXISTS PERSON (name varchar(50) PRIMARY KEY, score integer, date_of_birth date, registered timestamp)");
      stmt.executeUpdate("CREATE TABLE IF NOT EXISTS ADDRESS (address_id integer PRIMARY KEY, full_address varchar(255) NOT NULL);");
      stmt.executeUpdate("INSERT INTO PERSON (name,score) values (\"FRED\",21)");
      stmt.executeUpdate("INSERT INTO PERSON (name,score) values(\"JOSEPH\",34)");
      stmt.executeUpdate("INSERT INTO PERSON (name,score) values(\"MARMADUKE\",25)");

      stmt.executeUpdate("INSERT INTO ADDRESS (ADDRESS_ID, FULL_ADDRESS) values(1,\"57 Something St, El Barrio, Big Place\")");
      stmt.executeUpdate("INSERT INTO ADDRESS (ADDRESS_ID, FULL_ADDRESS) values(2,\"103 Bumblebee Ave, Jumpdown, Townie\")");

    }
	
    return con;
}

private static void printDatabase(Connection con) throws Exception
{
  Statement stmt = con.createStatement();
  ResultSet result = stmt.executeQuery("SELECT * FROM PERSON");
  while(result.next())
  {
    String name = result.getString("name");
    int score = result.getInt("score");
    System.out.println("NAME: " + name + " SCORE: " + score);
  }
  result.close();
  stmt.close();
}

static final ArrayList<ArrayList<Integer>> MATRIX = getArray();
static final ArrayList<ArrayList<Integer>> MATRIX_A = getArray();
static final ArrayList<ArrayList<Integer>> MATRIX_B = getArray();

static final int ROWS = 3;
static final int COLS = 3;

static final String FILE_PATH = "../code_comparator/building_blocks/grade.txt";
static final String URL_STRING = "https://www.google.se54";

  
  public static void main(String[] args)
  {
  
    Timer timer = new Timer();
    TimerTask task = new Helper();

    timer.schedule(task,20000);
Observable.just(FILE_PATH)
.map(filePath -> new FileReader(filePath))
.map(fileRead -> new BufferedReader(fileRead))
.flatMap(bufRead -> Observable.fromIterable(bufRead.lines()::iterator))
.map(line -> Arrays.asList(line.split("")))
.flatMap(word -> Observable.fromIterable(word))
.map(integer -> Integer.valueOf(integer))
.reduce((x,y) -> x + y)
.subscribe(System.out::println,
  error -> System.out.println("Error encountered parsing integers from file."));  timer.cancel();  

  }
}
