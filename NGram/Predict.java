import java.io.IOException;
import java.util.*;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

public class Predict {

 public static class Map extends Mapper<LongWritable, Text, Text, IntWritable> {
    private IntWritable p = new IntWritable(0);
    private Text word = new Text();
    private String[] prefix = new String[4];

    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString().toLowerCase().trim();
        //String pattern = "[^a-z]+";
        //line = line.replaceAll(pattern, " ").trim();
        if(line.length() == 0) return;
        String[] parts = line.split("\\t");
        String gram = parts[0];
        int count = Integer.parseInt(parts[1]);
        //String pattern = gram+"\\s";
        String[] words = gram.split("\\s");
        int len = words.length;

        for(int i=0;i<len-1;i++){
            int prob = count;
            p.set(prob);
            String output = prefix[i]+"\t"+gram;
            word.set(output);
            context.write(word, p);
        }

        if(len<5){
            prefix[len-1]=gram;
        }

    }
 }

 public static class Reduce extends Reducer<Text, IntWritable, Text, IntWritable> {

    public void reduce(Text key, Iterable<IntWritable> values, Context context)
      throws IOException, InterruptedException {
        int sum = 0;
        for (IntWritable val : values) {
            sum += val.get();
        }
        context.write(key, new IntWritable(sum));
    }
 }

 public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();

    Job job = new Job(conf, "wordcount");
    job.setJarByClass(Predict.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);

    job.setMapperClass(Map.class);
    job.setReducerClass(Reduce.class);

    job.setInputFormatClass(TextInputFormat.class);
    job.setOutputFormatClass(TextOutputFormat.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));

    job.waitForCompletion(true);
 }

}

