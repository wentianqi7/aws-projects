import java.io.IOException;
import java.util.*;

import org.apache.hadoop.mapreduce.lib.input.FileSplit;        
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
        
public class InvertedIndex {
       
 public static class Map extends Mapper<LongWritable, Text, Text, Text> {
    private Text word = new Text();
        
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString().toLowerCase();
        String pattern = "[\\W_]+";
        line = line.replaceAll(pattern, " ");
	    FileSplit fs = (FileSplit) context.getInputSplit();
	    String location = fs.getPath().getName();
        StringTokenizer tokenizer = new StringTokenizer(line);
        while (tokenizer.hasMoreTokens()) {
            word.set(tokenizer.nextToken());
            context.write(word, new Text(location));
        }
    }
 } 
        
 public static class Reduce extends Reducer<Text, Text, Text, Text> {

    public void reduce(Text key, Iterable<Text> values, Context context) 
      throws IOException, InterruptedException {
        StringBuilder output = new StringBuilder();
        HashSet<String> hash = new HashSet<String>();
        for(Text val : values){
            String tempVal = val.toString();
            if(hash.contains(tempVal)) continue;
            hash.add(tempVal);
            if(!output.toString().isEmpty()) output.append(", ");
            output.append(tempVal);
        } 
        context.write(new Text(key.toString()+" :"), new Text(output.toString()));
    }
 }
        
 public static void main(String[] args) throws Exception {
    //Configuration conf = new Configuration();
        
    Job job = new Job();
    job.setJarByClass(InvertedIndex.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Text.class);
        
    job.setMapperClass(Map.class);
    job.setReducerClass(Reduce.class);
        
    job.setInputFormatClass(TextInputFormat.class);
    job.setOutputFormatClass(TextOutputFormat.class);
        
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
        
    job.waitForCompletion(true);
 }
        
}

