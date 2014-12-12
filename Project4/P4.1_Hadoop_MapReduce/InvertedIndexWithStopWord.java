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
import org.apache.hadoop.filecache.DistributedCache;
import java.net.URI;
import java.io.*;        

public class InvertedIndexWithStopWord {
       
 public static class Map extends Mapper<LongWritable, Text, Text, Text> {
    private Text word = new Text();
        
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString().toLowerCase().trim();
        if(line == "") return;

        Path[] cacheFiles = DistributedCache.getLocalCacheFiles(context.getConfiguration());
        FileInputStream fileStream = new FileInputStream(cacheFiles[0].toString());
        BufferedReader reader = new BufferedReader(new InputStreamReader((InputStream) fileStream));
        String stop = null;
        while ((stop = reader.readLine()) != null) {
            String stop_pattern = "(\\b)"+stop+"(\\b)";
            line = line.replaceAll(stop_pattern, "$1$2");
        }

        String pattern = "[\\W_]+";
        String[] words = line.trim().split(pattern);
	    FileSplit fs = (FileSplit) context.getInputSplit();
	    String location = fs.getPath().getName();
        for(String w : words) {
            word.set(w);
            context.write(word, new Text(location));
        }
    }
 } 
        
 public static class Reduce extends Reducer<Text, Text, Text, Text> {

    public void reduce(Text key, Iterable<Text> values, Context context) 
      throws IOException, InterruptedException {
        if(key.toString().trim() == "") return;
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
    job.setJarByClass(InvertedIndexWithStopWord.class);
    DistributedCache.addCacheFile(new URI("hdfs:/english.stop"), job.getConfiguration());
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

